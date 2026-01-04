"""
Document Management Script
Add, update, delete, and list individual documents
"""
import os
import sys
import argparse
import logging
from pathlib import Path
from tabulate import tabulate
import psycopg2
from index_documents import (
    index_document,
    get_db_connection,
    delete_document_chunks
)
from config import Config

logger = logging.getLogger(__name__)


def add_document(file_path: str) -> bool:
    """Add a new document to the database"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"📄 Adding document: {Path(file_path).name}")
    return index_document(file_path, force=False)


def update_document(file_path: str) -> bool:
    """Update an existing document"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔄 Updating document: {Path(file_path).name}")
    return index_document(file_path, force=True)


def delete_document(document_name: str) -> bool:
    """Delete a document from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if document exists
        cursor.execute(
            "SELECT id FROM document_registry WHERE document_name = %s",
            (document_name,)
        )
        
        if not cursor.fetchone():
            print(f"❌ Document not found: {document_name}")
            cursor.close()
            conn.close()
            return False
        
        # Delete chunks
        delete_document_chunks(conn, document_name)
        
        # Update registry status
        cursor.execute(
            "UPDATE document_registry SET status = 'deleted', last_updated = CURRENT_TIMESTAMP WHERE document_name = %s",
            (document_name,)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Successfully deleted: {document_name}")
        return True
    
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        print(f"❌ Error: {e}")
        return False


def list_documents():
    """List all documents in the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                document_name,
                document_type,
                total_chunks,
                upload_date,
                last_updated,
                status
            FROM document_registry
            ORDER BY last_updated DESC
        """)
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not rows:
            print("\n📚 No documents found in the database")
            return
        
        # Format data for table
        headers = ["Document Name", "Type", "Chunks", "Uploaded", "Last Updated", "Status"]
        table_data = []
        
        for row in rows:
            doc_name, doc_type, chunks, uploaded, updated, status = row
            table_data.append([
                doc_name,
                doc_type,
                chunks,
                uploaded.strftime("%Y-%m-%d %H:%M"),
                updated.strftime("%Y-%m-%d %H:%M"),
                status
            ])
        
        print("\n📚 Documents in Database:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal: {len(rows)} documents\n")
    
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        print(f"❌ Error: {e}")


def show_statistics():
    """Show database statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total documents
        cursor.execute("SELECT COUNT(*) FROM document_registry WHERE status = 'active'")
        total_docs = cursor.fetchone()[0]
        
        # Total chunks
        cursor.execute("SELECT COUNT(*) FROM law_documents")
        total_chunks = cursor.fetchone()[0]
        
        # Database size
        cursor.execute("""
            SELECT pg_size_pretty(pg_total_relation_size('law_documents')) as size
        """)
        db_size = cursor.fetchone()[0]
        
        # Documents by type
        cursor.execute("""
            SELECT document_type, COUNT(*) 
            FROM document_registry 
            WHERE status = 'active'
            GROUP BY document_type
        """)
        docs_by_type = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Display statistics
        print("\n" + "="*60)
        print("📊 Database Statistics")
        print("="*60)
        print(f"Total Documents: {total_docs}")
        print(f"Total Chunks: {total_chunks}")
        print(f"Database Size: {db_size}")
        print("\nDocuments by Type:")
        for doc_type, count in docs_by_type:
            print(f"  - {doc_type}: {count}")
        print("="*60 + "\n")
    
    except Exception as e:
        logger.error(f"Error showing statistics: {e}")
        print(f"❌ Error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Manage Pakistani cyber law documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a new document
  python manage_documents.py --add data/raw/PECA_2016.pdf
  
  # Update an existing document
  python manage_documents.py --update data/raw/PECA_2016.pdf
  
  # Delete a document
  python manage_documents.py --delete "PECA_2016.pdf"
  
  # List all documents
  python manage_documents.py --list
  
  # Show statistics
  python manage_documents.py --stats
        """
    )
    
    parser.add_argument('--add', type=str, help='Add a new document')
    parser.add_argument('--update', type=str, help='Update an existing document')
    parser.add_argument('--delete', type=str, help='Delete a document by name')
    parser.add_argument('--list', action='store_true', help='List all documents')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    
    args = parser.parse_args()
    
    # Check if at least one argument is provided
    if not any([args.add, args.update, args.delete, args.list, args.stats]):
        parser.print_help()
        sys.exit(0)
    
    try:
        # Validate configuration
        Config.validate()
        
        print("\n🇵🇰 Pakistani Cyber Law Document Manager")
        print("="*60)
        
        # Execute commands
        if args.add:
            add_document(args.add)
        
        if args.update:
            update_document(args.update)
        
        if args.delete:
            delete_document(args.delete)
        
        if args.list:
            list_documents()
        
        if args.stats:
            show_statistics()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
