"""
Document Indexing Script for ChromaDB
Bulk indexing of Pakistani cyber law documents
NO DATABASE SERVER NEEDED!
"""
import os
import sys
import hashlib
import json
import logging
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
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
            loader = TextLoader(file_path, encoding='utf-8')
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


def load_document_registry():
    """Load document registry from JSON file"""
    registry_file = Path(Config.PROCESSED_DATA_DIR) / "document_registry.json"
    if registry_file.exists():
        with open(registry_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_document_registry(registry):
    """Save document registry to JSON file"""
    registry_file = Path(Config.PROCESSED_DATA_DIR) / "document_registry.json"
    registry_file.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_file, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, default=str)


def index_document(file_path: str, vectorstore, force: bool = False) -> bool:
    """
    Index a single document into ChromaDB
    
    Args:
        file_path: Path to the document
        vectorstore: ChromaDB vectorstore instance
        force: Force re-indexing even if unchanged
    
    Returns:
        True if indexed successfully, False otherwise
    """
    try:
        # Get document info
        document_name = Path(file_path).name
        document_type = Path(file_path).suffix.lower().replace('.', '')
        file_hash = calculate_file_hash(file_path)
        
        # Load registry
        registry = load_document_registry()
        
        # Check if document exists and has changed
        if document_name in registry:
            if registry[document_name]['file_hash'] == file_hash and not force:
                logger.info(f"Skipping {document_name} (unchanged)")
                return True
        
        logger.info(f"Processing {document_name}...")
        
        # Load and split document
        documents = load_document(file_path)
        if not documents:
            return False
        
        chunks = split_documents(documents)
        if not chunks:
            logger.warning(f"No chunks created for {document_name}")
            return False
        
        # Add metadata to chunks
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                'source': document_name,
                'document_name': document_name,
                'document_type': document_type,
                'chunk_index': i,
                'file_path': str(file_path)
            })
        
        # Add to vectorstore
        vectorstore.add_documents(chunks)
        
        # Update registry
        registry[document_name] = {
            'file_path': str(file_path),
            'file_hash': file_hash,
            'document_type': document_type,
            'total_chunks': len(chunks),
            'indexed_at': str(Path(file_path).stat().st_mtime)
        }
        save_document_registry(registry)
        
        logger.info(f"Successfully indexed {document_name} ({len(chunks)} chunks)")
        return True
    
    except Exception as e:
        logger.error(f"Error indexing {file_path}: {e}")
        return False


def index_all_documents(force: bool = False):
    """Index all documents in the raw data directory"""
    # Create data directories if they don't exist
    os.makedirs(Config.RAW_DATA_DIR, exist_ok=True)
    os.makedirs(Config.PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(Config.CHROMA_PERSIST_DIR, exist_ok=True)
    
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
    
    # Initialize embeddings and vectorstore
    print("\n🔄 Initializing ChromaDB...")
    embeddings = HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    vectorstore = Chroma(
        collection_name=Config.CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=Config.CHROMA_PERSIST_DIR
    )
    
    print(f"✅ ChromaDB initialized at: {Config.CHROMA_PERSIST_DIR}")
    
    # Index each document
    success_count = 0
    for file_path in files:
        print(f"\n📄 Processing: {file_path.name}")
        if index_document(str(file_path), vectorstore, force=force):
            success_count += 1
            print(f"   ✅ Successfully indexed")
        else:
            print(f"   ❌ Failed to index")
    
    print(f"\n{'='*60}")
    print(f"✨ Indexing complete: {success_count}/{len(files)} documents indexed")
    print(f"📁 ChromaDB location: {Config.CHROMA_PERSIST_DIR}")
    print(f"{'='*60}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Index Pakistani cyber law documents into ChromaDB")
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-indexing of all documents'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate configuration
        Config.validate()
        
        print("🇵🇰 Pakistani Cyber Law Document Indexer (ChromaDB)")
        print("="*60)
        print("✅ NO DATABASE SERVER NEEDED!")
        print("="*60)
        
        # Index all documents
        index_all_documents(force=args.force)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
