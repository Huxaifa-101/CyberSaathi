"""
Centralized configuration for Pakistani Cyber Law Chatbot
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # ChromaDB Configuration
    CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "pak_cyberlaw_docs")
    CHROMA_PERSIST_DIR = os.getenv(
        "CHROMA_PERSIST_DIR", 
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "chroma_db")
    )
    
    # Embedding Model
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL", 
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", 384))
    
    # Retrieval Configuration
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", 10))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    
    # LLM Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash-exp")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        errors = []
        
        if not cls.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY is not set")
        
        if not cls.TAVILY_API_KEY:
            errors.append("TAVILY_API_KEY is not set")
        
        if errors:
            raise ValueError(
                "Configuration errors:\n" + "\n".join(f"- {e}" for e in errors)
            )
        
        return True
    
    @classmethod
    def setup_logging(cls):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger(__name__)

# Create logger instance
logger = Config.setup_logging()
