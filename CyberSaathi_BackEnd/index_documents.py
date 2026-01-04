"""
Document Indexing Script
Bulk indexing of Pakistani cyber law documents into PostgreSQL
"""
import os
import sys
import hashlib
import logging
from pathlib import Path
from typing import List, Dict
import psycopg2
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config

logger = logging.getLogger(__name__)


def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def load_document(file_path: str) -> List:
    """Load a document based on its extension"""
    file_ext = Path(file_path).suffix.lower()
    
    try:
        if file_ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_ext in ['.docx', '.doc']:
            loader = Docx2txtLoader(file_path)
        elif file_ext == '.txt':
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_ext}")
            return []
        
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} pages from {Path(file_path).name}")
        return documents
    
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return []


def split_documents(documents: List, chunk_size: int = None, chunk_overlap: int = None) -> List:
    """Split documents into chunks"""
    if chunk_size is None:
        chunk_size = Config.CHUNK_SIZE
    if chunk_overlap is None:
        chunk_overlap = Config.CHUNK_OVERLAP
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split into {len(chunks)} chunks")
    return chunks


def get_db_connection():
    """Get PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT,
            database=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise


def check_document_exists(conn, document_name: str, file_hash: str) -> Dict:
    """Check if document exists and if it has changed"""
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, file_hash, total_chunks FROM document_registry WHERE document_name = %s",
        (document_name,)
    )
    
    result = cursor.fetchone()
    cursor.close()
    
    if result:
        existing_id, existing_hash, total_chunks = result
        return {
            "exists": True,
            "id": existing_id,
            "changed": existing_hash != file_hash,
            "total_chunks": total_chunks
        }
    else:
        return {"exists": False, "changed": True}


def delete_document_chunks(conn, document_name: str):
    """Delete all chunks for a document"""
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM law_documents WHERE document_name = %s",
        (document_name,)
    )
    conn.commit()
    deleted_count = cursor.rowcount
    cursor.close()
    logger.info(f"Deleted {deleted_count} chunks for {document_name}")


def insert_chunks(conn, document_name: str, document_type: str, chunks: List, embeddings_model):
    """Insert document chunks with embeddings into database"""
    cursor = conn.cursor()
    
    # Generate embeddings for all chunks
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embeddings_model.embed_documents(texts)
    
    # Insert chunks
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        metadata = chunk.metadata
        metadata['chunk_index'] = i
        
        cursor.execute(
            """
            INSERT INTO law_documents 
            (document_name, document_type, chunk_text, chunk_index, metadata, embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                document_name,
                document_type,
                chunk.page_content,
                i,
                psycopg2.extras.Json(metadata),
                embedding
            )
        )
    
    conn.commit()
    cursor.close()
    logger.info(f"Inserted {len(chunks)} chunks for {document_name}")


def update_document_registry(conn, document_name: str, file_path: str, file_hash: str, 
                            document_type: str, total_chunks: int, status: str = "active"):
    """Update or insert document in registry"""
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO document_registry 
        (document_name, file_path, file_hash, document_type, total_chunks, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (document_name) 
        DO UPDATE SET
            file_path = EXCLUDED.file_path,
            file_hash = EXCLUDED.file_hash,
            document_type = EXCLUDED.document_type,
            total_chunks = EXCLUDED.total_chunks,
            last_updated = CURRENT_TIMESTAMP,
            status = EXCLUDED.status
        """,
        (document_name, file_path, file_hash, document_type, total_chunks, status)
    )
    
    conn.commit()
    cursor.close()
    logger.info(f"Updated registry for {document_name}")


def index_document(file_path: str, force: bool = False) -> bool:
    """
    Index a single document
    
    Args:
        file_path: Path to the document
        force: Force re-indexing even if unchanged
    
    Returns:
        True if indexed successfully, False otherwise
    """
    try:
        # Get document info
        document_name = Path(file_path).name
        document_type = Path(file_path).suffix.lower().replace('.', '')
        file_hash = calculate_file_hash(file_path)
        
        # Connect to database
        conn = get_db_connection()
        
        # Check if document exists and has changed
        doc_info = check_document_exists(conn, document_name, file_hash)
        
        if doc_info["exists"] and not doc_info["changed"] and not force:
            logger.info(f"Skipping {document_name} (unchanged)")
            conn.close()
            return True
        
        logger.info(f"Processing {document_name}...")
        
        # Load and split document
        documents = load_document(file_path)
        if not documents:
            conn.close()
            return False
        
        chunks = split_documents(documents)
        if not chunks:
            logger.warning(f"No chunks created for {document_name}")
            conn.close()
            return False
        
        # Initialize embeddings
        embeddings_model = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Delete old chunks if updating
        if doc_info["exists"]:
            delete_document_chunks(conn, document_name)
        
        # Insert new chunks
        insert_chunks(conn, document_name, document_type, chunks, embeddings_model)
        
        # Update registry
        update_document_registry(
            conn, document_name, file_path, file_hash, 
            document_type, len(chunks)
        )
        
        conn.close()
        logger.info(f"Successfully indexed {document_name}")
        return True
    
    except Exception as e:
        logger.error(f"Error indexing {file_path}: {e}")
        return False


def index_all_documents(force: bool = False):
    """Index all documents in the raw data directory"""
    # Create data directories if they don't exist
    os.makedirs(Config.RAW_DATA_DIR, exist_ok=True)
    os.makedirs(Config.PROCESSED_DATA_DIR, exist_ok=True)
    
    # Get all supported files
    supported_extensions = ['.pdf', '.docx', '.doc', '.txt']
    files = []
    
    for ext in supported_extensions:
        files.extend(Path(Config.RAW_DATA_DIR).glob(f'*{ext}'))
    
    if not files:
        logger.warning(f"No documents found in {Config.RAW_DATA_DIR}")
        print(f"\n⚠️  No documents found in {Config.RAW_DATA_DIR}")
        print("Please add PDF, DOCX, or TXT files to the data/raw/ directory")
        return
    
    logger.info(f"Found {len(files)} documents to process")
    print(f"\n📚 Found {len(files)} documents to index")
    
    # Index each document
    success_count = 0
    for file_path in files:
        print(f"\n📄 Processing: {file_path.name}")
        if index_document(str(file_path), force=force):
            success_count += 1
            print(f"   ✅ Successfully indexed")
        else:
            print(f"   ❌ Failed to index")
    
    print(f"\n{'='*60}")
    print(f"✨ Indexing complete: {success_count}/{len(files)} documents indexed")
    print(f"{'='*60}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Index Pakistani cyber law documents")
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-indexing of all documents'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate configuration
        Config.validate()
        
        print("🇵🇰 Pakistani Cyber Law Document Indexer")
        print("="*60)
        
        # Index all documents
        index_all_documents(force=args.force)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
