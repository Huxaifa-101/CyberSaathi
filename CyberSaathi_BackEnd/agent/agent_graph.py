"""
Agent Graph - LangGraph-based Routing and Generation
Routes queries to law retrieval or web search, then generates answers
"""
import logging
from typing import TypedDict, Annotated, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from config import Config
from tools.law_retriever import law_retrieval_tool
from tools.web_search import web_search_tool
from privacy.pii_detector import sanitize_query
from privacy.redaction_logger import RedactionLogger

logger = logging.getLogger(__name__)

# Initialize redaction logger
redaction_logger = RedactionLogger(log_file="logs/pii_redactions.log")


# Define the state
class AgentState(TypedDict):
    """State for the agent graph"""
    messages: Annotated[list, add_messages]
    query: str
    original_query: str  # Original query before sanitization
    sanitized_query: str  # Query after PII redaction
    redaction_info: dict  # Information about what was redacted
    context: str
    source_tool: str
    source_documents: list  # List of source documents used
    answer: str


def create_llm():
    """Create the LLM instance"""
    return ChatGoogleGenerativeAI(
        model=Config.LLM_MODEL,
        temperature=Config.LLM_TEMPERATURE,
        google_api_key=Config.GOOGLE_API_KEY
    )


def sanitization_node(state: AgentState) -> AgentState:
    """
    Sanitize the query by detecting and redacting PII
    This runs BEFORE any external API calls
    """
    original_query = state["query"]
    
    # Sanitize the query
    sanitized, redaction_info = sanitize_query(original_query, log_redactions=True)
    
    # Log redaction event
    if redaction_info.get("redacted"):
        redaction_logger.log_redaction(redaction_info)
        logger.warning(
            f"PII detected and redacted from query. "
            f"Types: {', '.join(redaction_info.get('types_redacted', []))}, "
            f"Count: {redaction_info.get('redaction_count', 0)}"
        )
    
    # Update state
    state["original_query"] = original_query
    state["sanitized_query"] = sanitized
    state["redaction_info"] = redaction_info
    
    # Use sanitized query for all further processing
    state["query"] = sanitized
    
    logger.info("Query sanitization completed")
    return state


def router_node(state: AgentState) -> AgentState:
    """
    Route the query to either law retrieval or web search
    Uses the SANITIZED query
    """
    query = state["query"]  # This is now the sanitized query
    
    # Create routing prompt
    routing_prompt = f"""You are a routing assistant for a Pakistani cyber law chatbot.

Analyze the following query and determine if it should be answered using:
- "law" - Use the law database (for questions about Pakistani cyber laws, PECA, regulations, penalties, legal definitions)
- "web" - Use web search (for recent news, current cases, updates, or when explicitly asked to search the web)

Query: {query}

Respond with ONLY one word: either "law" or "web"
"""
    
    llm = create_llm()
    response = llm.invoke([HumanMessage(content=routing_prompt)])
    
    # Parse the response
    route = response.content.strip().lower()
    if "web" in route:
        state["source_tool"] = "web"
    else:
        state["source_tool"] = "law"
    
    logger.info(f"Routed query to: {state['source_tool']}")
    return state


def law_retrieval_node(state: AgentState) -> AgentState:
    """
    Retrieve information from the law database
    Also extracts source document information
    """
    query = state["query"]
    
    try:
        # Get retriever and retrieve documents
        from tools.law_retriever import get_law_retriever
        retriever = get_law_retriever()
        documents = retriever.invoke(query)
        
        # Extract source documents
        source_docs = []
        seen_docs = set()
        
        for doc in documents:
            doc_name = doc.metadata.get('document_name', 'Unknown')
            if doc_name not in seen_docs:
                source_docs.append({
                    'name': doc_name,
                    'type': doc.metadata.get('document_type', 'unknown')
                })
                seen_docs.add(doc_name)
        
        # Format context
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('document_name', 'Unknown')
            text = doc.page_content
            context_parts.append(f"[Source {i}: {source}]\n{text}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        state["context"] = context
        state["source_documents"] = source_docs
        logger.info(f"Law retrieval completed with {len(source_docs)} source documents")
    except Exception as e:
        logger.error(f"Error in law retrieval node: {e}")
        state["context"] = f"Error retrieving law information: {str(e)}"
        state["source_documents"] = []
    
    return state


def web_search_node(state: AgentState) -> AgentState:
    """
    Search the web for information
    """
    query = state["query"]
    
    try:
        context = web_search_tool.invoke({"query": query})
        state["context"] = context
        state["source_documents"] = []  # Web search doesn't use law documents
        logger.info("Web search completed")
    except Exception as e:
        logger.error(f"Error in web search node: {e}")
        state["context"] = f"Error performing web search: {str(e)}"
        state["source_documents"] = []
    
    return state


def generation_node(state: AgentState) -> AgentState:
    """
    Generate the final answer using the retrieved context
    """
    query = state["query"]
    context = state["context"]
    source_tool = state["source_tool"]
    redaction_info = state.get("redaction_info", {})
    source_documents = state.get("source_documents", [])
    
    # Create generation prompt
    system_prompt = """You are CyberSaathi, an expert assistant on Pakistani cyber laws and cybercrime regulations.

Your role is to:
- Provide accurate, helpful information about Pakistani cyber laws
- Cite specific laws, sections, and penalties when applicable
- Explain legal concepts in clear, understandable language
- Be professional and informative
- If you don't have enough information, say so clearly

Always base your answer on the provided context. If the context doesn't contain relevant information, acknowledge this limitation.
"""
    
    user_prompt = f"""Based on the following context, answer the user's question about Pakistani cyber law.

Context:
{context}

User Question: {query}

Provide a clear, accurate, and helpful answer. If the context is from law documents, cite specific sections or laws. If from web search, mention that the information is from recent sources.
"""
    
    llm = create_llm()
    
    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        answer = response.content
        
        # Add source citations if from law documents
        if source_tool == "law" and source_documents:
            citations = "\n\n---\n**📚 Sources:**\n"
            for i, doc in enumerate(source_documents, 1):
                doc_name = doc['name']
                doc_type = doc.get('type', 'unknown').upper()
                citations += f"{i}. {doc_name} ({doc_type})\n"
            answer = answer + citations
        
        # Add privacy notice if PII was redacted
        if redaction_info.get("redacted"):
            privacy_notice = (
                "\n---\n"
                "🔒 **Privacy Notice**: For your protection, sensitive personal information "
                "was automatically detected and removed from your query before processing. "
                f"({redaction_info.get('redaction_count', 0)} item(s) redacted). "
                "Your confidential data was never sent to external services."
            )
            answer = answer + privacy_notice
        
        state["answer"] = answer
        logger.info("Answer generation completed")
    except Exception as e:
        logger.error(f"Error in generation node: {e}")
        state["answer"] = f"Error generating answer: {str(e)}"
    
    return state


def route_after_router(state: AgentState) -> Literal["law_retrieval", "web_search"]:
    """
    Conditional edge to route to the appropriate retrieval node
    """
    if state["source_tool"] == "web":
        return "web_search"
    else:
        return "law_retrieval"


def create_agent_graph():
    """
    Create the agent graph with PII sanitization, routing and generation
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("sanitization", sanitization_node)  # NEW: First step
    workflow.add_node("router", router_node)
    workflow.add_node("law_retrieval", law_retrieval_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("generation", generation_node)
    
    # Add edges
    workflow.set_entry_point("sanitization")  # Start with sanitization
    workflow.add_edge("sanitization", "router")  # Then route
    
    # Conditional routing after router
    workflow.add_conditional_edges(
        "router",
        route_after_router,
        {
            "law_retrieval": "law_retrieval",
            "web_search": "web_search"
        }
    )
    
    # Both retrieval nodes go to generation
    workflow.add_edge("law_retrieval", "generation")
    workflow.add_edge("web_search", "generation")
    
    # Generation goes to end
    workflow.add_edge("generation", END)
    
    # Compile the graph
    app = workflow.compile()
    
    logger.info("Agent graph created successfully")
    return app


def run_agent(query: str) -> dict:
    """
    Run the agent with a query
    
    Args:
        query: User's question
    
    Returns:
        Dictionary with answer, context, and source_tool
    """
    try:
        # Create the graph
        app = create_agent_graph()
        
        # Initialize state
        initial_state = {
            "messages": [],
            "query": query,
            "original_query": "",
            "sanitized_query": "",
            "redaction_info": {},
            "context": "",
            "source_tool": "",
            "source_documents": [],
            "answer": ""
        }
        
        # Run the graph
        result = app.invoke(initial_state)
        
        return {
            "answer": result["answer"],
            "context": result["context"],
            "source_tool": result["source_tool"],
            "source_documents": result.get("source_documents", []),
            "pii_redacted": result.get("redaction_info", {}).get("redacted", False),
            "redaction_info": result.get("redaction_info", {})
        }
    
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        return {
            "answer": f"An error occurred: {str(e)}",
            "context": "",
            "source_tool": "error"
        }
