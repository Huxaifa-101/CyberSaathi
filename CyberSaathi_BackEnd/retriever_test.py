"""
Retriever Test Script
Test the law retrieval functionality
"""
import logging
from tools.law_retriever import get_law_retriever, search_with_filter
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_basic_retrieval():
    """Test basic retrieval functionality"""
    print("\n" + "="*60)
    print("🔍 Testing Basic Retrieval")
    print("="*60)
    
    try:
        # Validate config
        Config.validate()
        
        # Test queries
        test_queries = [
            "What are the penalties for unauthorized access?",
            "Tell me about PECA 2016",
            "What is cybercrime?"
        ]
        
        retriever = get_law_retriever(k=3)
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            print("-" * 60)
            
            documents = retriever.invoke(query)
            
            if documents:
                print(f"✅ Retrieved {len(documents)} documents\n")
                for i, doc in enumerate(documents, 1):
                    source = doc.metadata.get('document_name', 'Unknown')
                    text = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                    print(f"{i}. Source: {source}")
                    print(f"   Content: {text}\n")
            else:
                print("❌ No documents retrieved\n")
    
    except Exception as e:
        logger.error(f"Error in basic retrieval test: {e}")
        print(f"❌ Error: {e}")


def test_filtered_search():
    """Test filtered search functionality"""
    print("\n" + "="*60)
    print("🔍 Testing Filtered Search")
    print("="*60)
    
    try:
        query = "unauthorized access"
        
        # Test without filter
        print(f"\n📝 Query: {query} (no filter)")
        print("-" * 60)
        results = search_with_filter(query, k=3)
        print(f"✅ Retrieved {len(results)} documents\n")
        
        # Test with filter (example - adjust based on your documents)
        # print(f"\n📝 Query: {query} (filtered by document)")
        # print("-" * 60)
        # results = search_with_filter(
        #     query, 
        #     filters={"document_name": "PECA_2016.pdf"},
        #     k=3
        # )
        # print(f"✅ Retrieved {len(results)} documents\n")
    
    except Exception as e:
        logger.error(f"Error in filtered search test: {e}")
        print(f"❌ Error: {e}")


def main():
    """Main entry point"""
    print("\n🇵🇰 Pakistani Cyber Law Retriever Test")
    
    try:
        test_basic_retrieval()
        test_filtered_search()
        
        print("\n" + "="*60)
        print("✅ Testing Complete")
        print("="*60 + "\n")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Fatal Error: {e}\n")


if __name__ == "__main__":
    main()
