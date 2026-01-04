"""
FastAPI REST API for Pakistani Cyber Law Chatbot
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from agent.agent_graph import run_agent
from config import Config

# Setup logging
logger = logging.getLogger(__name__)

# Validate configuration on startup
try:
    Config.validate()
    logger.info("Configuration validated successfully")
except Exception as e:
    logger.error(f"Configuration validation failed: {e}")
    raise

# Create FastAPI app
api = FastAPI(
    title="CyberSaathi - Pakistani Cyber Law Chatbot",
    description="RAG-based chatbot for Pakistani cybercrime laws and regulations",
    version="1.0.0"
)

# Add CORS middleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    """Chat request model"""
    query: str = Field(..., description="User's question about Pakistani cyber law")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the penalties for unauthorized access under PECA 2016?"
            }
        }


class ChatResponse(BaseModel):
    """Chat response model"""
    answer: str = Field(..., description="Generated answer")
    context: str = Field(..., description="Retrieved context used for answer")
    source_tool: str = Field(..., description="Tool used: 'law' or 'web'")
    source_documents: List[Dict[str, str]] = Field(default=[], description="List of source documents used")
    pii_redacted: bool = Field(default=False, description="Whether PII was detected and redacted")
    redaction_count: int = Field(default=0, description="Number of PII items redacted")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Under Section 3 of PECA 2016...\n\n---\n📚 Sources:\n1. PECA_2016.pdf (PDF)",
                "context": "Section 3 - Unauthorized access to information system...",
                "source_tool": "law",
                "source_documents": [
                    {"name": "PECA_2016.pdf", "type": "pdf"}
                ],
                "pii_redacted": False,
                "redaction_count": 0
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str


# Routes
@api.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return {
        "status": "online",
        "message": "CyberSaathi API is running. Use POST /chat to ask questions."
    }


@api.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is operational"
    }


@api.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - Ask questions about Pakistani cyber law
    
    Args:
        request: ChatRequest with user query
    
    Returns:
        ChatResponse with answer, context, and source
    """
    try:
        logger.info(f"Received query: {request.query[:100]}...")
        
        # Validate query
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty"
            )
        
        # Run the agent
        result = run_agent(request.query)
        
        logger.info(f"Query processed successfully using {result['source_tool']}")
        
        return ChatResponse(
            answer=result["answer"],
            context=result["context"],
            source_tool=result["source_tool"],
            source_documents=result.get("source_documents", []),
            pii_redacted=result.get("pii_redacted", False),
            redaction_count=result.get("redaction_info", {}).get("redaction_count", 0)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@api.get("/info")
async def info():
    """Get API information"""
    return {
        "name": "CyberSaathi",
        "description": "Pakistani Cyber Law Chatbot",
        "version": "1.0.0",
        "llm_model": Config.LLM_MODEL,
        "embedding_model": Config.EMBEDDING_MODEL,
        "database": "ChromaDB"
    }


# Run with: uvicorn api:api --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)
