"""
Law Retriever Tool - ChromaDB Vector Retrieval
Retrieves relevant Pakistani cyber law documents from ChromaDB
"""
import logging
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import tool
from config import Config

logger = logging.getLogger(__name__)


def get_law_retriever(k: int = None):
    """
    Create a law retriever using ChromaDB
    
    Args:
        k: Number of documents to retrieve (default from config)
    
    Returns:
        LangChain retriever instance
    """
    if k is None:
        k = Config.RETRIEVAL_K
    
    try:
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize ChromaDB store
        vectorstore = Chroma(
            collection_name=Config.CHROMA_COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=Config.CHROMA_PERSIST_DIR
        )
        
        # Create retriever
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        
        logger.info(f"Law retriever initialized successfully with k={k}")
        return retriever
    
    except Exception as e:
        logger.error(f"Error initializing law retriever: {e}")
        raise


@tool
def law_retrieval_tool(query: str) -> str:
    """
    Retrieve relevant Pakistani cyber law information from ChromaDB.
    
    Use this tool when the user asks about:
    - Pakistani cyber laws (PECA, cybercrime regulations)
    - Legal penalties and punishments
    - Cybercrime definitions and classifications
    - Legal procedures and requirements
    - Rights and obligations under cyber law
    
    Args:
        query: The user's question about Pakistani cyber law
    
    Returns:
        Relevant law excerpts and information
    """
    try:
        retriever = get_law_retriever()
        documents = retriever.invoke(query)
        
        if not documents:
            return "No relevant law information found in the database."
        
        # Format the retrieved documents
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', doc.metadata.get('document_name', 'Unknown'))
            text = doc.page_content
            context_parts.append(f"[Source {i}: {source}]\n{text}")
        
        context = "\n\n---\n\n".join(context_parts)
        logger.info(f"Retrieved {len(documents)} documents for query: {query[:50]}...")
        
        return context
    
    except Exception as e:
        logger.error(f"Error in law retrieval: {e}")
        return f"Error retrieving law information: {str(e)}"


def search_with_filter(query: str, filters: Dict[str, Any] = None, k: int = None) -> List[Dict]:
    """
    Advanced search with metadata filtering
    
    Args:
        query: Search query
        filters: Metadata filters (e.g., {"source": "PECA_2016.pdf"})
        k: Number of results
    
    Returns:
        List of matching documents with metadata
    """
    if k is None:
        k = Config.RETRIEVAL_K
    
    try:
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
        
        # Perform filtered search
        if filters:
            documents = vectorstore.similarity_search(
                query,
                k=k,
                filter=filters
            )
        else:
            documents = vectorstore.similarity_search(query, k=k)
        
        # Format results
        results = []
        for doc in documents:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        logger.info(f"Filtered search returned {len(results)} results")
        return results
    
    except Exception as e:
        logger.error(f"Error in filtered search: {e}")
        return []


def get_vectorstore():
    """
    Get the ChromaDB vectorstore instance
    
    Returns:
        Chroma vectorstore instance
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    return Chroma(
        collection_name=Config.CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=Config.CHROMA_PERSIST_DIR
    )
