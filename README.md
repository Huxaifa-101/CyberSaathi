# 🛡️ CyberSaathi - Pakistani Cyber Law AI Assistant

**An intelligent RAG-based chatbot providing expert guidance on Pakistani cybercrime laws and regulations with built-in privacy protection.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?logo=react)](https://react.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.13-1C3C3C)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5.0+-FF6F00)](https://www.trychroma.com/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
  - [Complete Query Execution Flow](#complete-query-execution-flow)
  - [Backend Workflow](#backend-workflow)
  - [Frontend Workflow](#frontend-workflow)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Privacy & Security](#-privacy--security)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**CyberSaathi** is an AI-powered chatbot designed to help users understand Pakistani cyber laws, including PECA 2016 (Prevention of Electronic Crimes Act) and related cybercrime regulations. It uses advanced RAG (Retrieval-Augmented Generation) techniques to provide accurate, context-aware responses while automatically protecting user privacy by detecting and redacting Personally Identifiable Information (PII).

### Key Capabilities

- 📚 **Legal Knowledge Base**: Comprehensive database of Pakistani cyber laws and regulations
- 🔍 **Intelligent Routing**: Automatically routes queries to law database or web search
- 🔒 **Privacy Protection**: Automatic PII detection and redaction before processing
- 📖 **Source Citations**: Transparent source attribution for all legal responses
- 🌐 **Web Search Integration**: Real-time information for recent cases and updates
- 💬 **Conversation History**: Persistent chat sessions with Supabase integration

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (React + TypeScript + Vite)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP POST /chat
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI REST API                           │
│                      (api.py - Port 8000)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ run_agent(query)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LANGGRAPH AGENT WORKFLOW                     │
│                     (agent/agent_graph.py)                      │
│                                                                 │
│  ┌──────────────┐    ┌──────────┐    ┌─────────────────────┐  │
│  │ Sanitization │───▶│  Router  │───▶│ Law / Web Retrieval │  │
│  │  (PII Check) │    │  (LLM)   │    │                     │  │
│  └──────────────┘    └──────────┘    └──────────┬──────────┘  │
│                                                   │             │
│                                      ┌────────────▼──────────┐  │
│                                      │   Answer Generation   │  │
│                                      │   (LLM + Citations)   │  │
│                                      └───────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
    ┌───────────────────┐     ┌──────────────────┐
    │   ChromaDB        │     │  Tavily Search   │
    │ (Vector Store)    │     │  (Web Search)    │
    │ - PECA 2016       │     │                  │
    │ - Cyber Laws      │     │                  │
    └───────────────────┘     └──────────────────┘
```

---

## ✨ Features

### 🤖 Intelligent Query Processing
- **Automatic Routing**: LLM-based decision making to route queries to appropriate data source
- **Context-Aware Responses**: RAG pipeline retrieves relevant legal documents before answering
- **Multi-Source Support**: Combines law database and web search for comprehensive answers

### 🔐 Privacy Protection
- **PII Detection**: Automatically detects 10+ types of sensitive information:
  - Pakistani CNIC numbers
  - Phone numbers
  - Email addresses
  - Bank account numbers
  - Credit card numbers
  - IP addresses
  - Names and addresses
  - Dates of birth
  - URLs with personal info
- **Automatic Redaction**: Removes PII before sending to external APIs
- **Audit Logging**: Tracks all redactions for compliance

### 📚 Source Attribution
- **Document Citations**: Every answer includes source documents used
- **Transparency**: Users can verify information against original sources
- **Metadata Tracking**: Document type, name, and relevance scores

### 💾 Data Persistence
- **Conversation History**: Supabase integration for chat persistence
- **Session Management**: Multiple conversation threads
- **Message Storage**: Complete chat history with timestamps

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Core language |
| **FastAPI** | 0.115.6 | REST API framework |
| **LangChain** | 0.3.13 | LLM orchestration |
| **LangGraph** | 0.2.60 | Agent workflow management |
| **ChromaDB** | 0.5.0+ | Vector database |
| **Google Gemini** | 2.0-flash-exp | LLM for generation |
| **HuggingFace** | all-MiniLM-L6-v2 | Embedding model |
| **Tavily** | 0.5.0 | Web search API |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.3.1 | UI framework |
| **TypeScript** | 5.5.3 | Type safety |
| **Vite** | 5.4.2 | Build tool |
| **TailwindCSS** | 3.4.1 | Styling |
| **Supabase** | 2.57.4 | Database & auth |
| **Lucide React** | 0.344.0 | Icons |

---

## 📁 Project Structure

```
CyberSaathi/
├── CyberSaathi_BackEnd/          # Python FastAPI Backend
│   ├── agent/                    # LangGraph agent logic
│   │   ├── __init__.py
│   │   └── agent_graph.py        # Main agent workflow
│   ├── privacy/                  # PII detection & redaction
│   │   ├── __init__.py
│   │   ├── pii_detector.py       # PII detection patterns
│   │   └── redaction_logger.py   # Audit logging
│   ├── tools/                    # LangChain tools
│   │   ├── __init__.py
│   │   ├── law_retriever.py      # ChromaDB retrieval
│   │   └── web_search.py         # Tavily search
│   ├── data/                     # Data storage
│   │   ├── raw/                  # Original documents
│   │   ├── chroma_db/            # Vector database
│   │   └── processed/            # Processed documents
│   ├── logs/                     # Application logs
│   ├── api.py                    # FastAPI application
│   ├── config.py                 # Configuration management
│   ├── index_documents_chromadb.py  # Document indexing
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Environment variables
│
├── CyberSaathi_FrontEnd/         # React TypeScript Frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── ChatContainer.tsx # Main chat interface
│   │   │   ├── ChatMessage.tsx   # Message display
│   │   │   ├── ChatInput.tsx     # User input
│   │   │   ├── ChatSidebar.tsx   # Conversation list
│   │   │   ├── Navigation.tsx    # Top navigation
│   │   │   ├── HeroSection.tsx   # Landing page hero
│   │   │   ├── FeatureCards.tsx  # Feature showcase
│   │   │   └── api.js            # API client
│   │   ├── lib/
│   │   │   └── supabase.ts       # Supabase client
│   │   ├── App.tsx               # Root component
│   │   ├── main.tsx              # Entry point
│   │   └── index.css             # Global styles
│   ├── package.json              # Node dependencies
│   ├── vite.config.ts            # Vite configuration
│   ├── tailwind.config.js        # Tailwind configuration
│   └── .env                      # Environment variables
│
└── README.md                     # This file
```

---

## 🔄 How It Works

### Complete Query Execution Flow

Here's the **end-to-end journey** of a user query through the system:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        STEP 1: USER INPUT                           │
└─────────────────────────────────────────────────────────────────────┘
User types: "What are the penalties for hacking under PECA 2016?"
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STEP 2: FRONTEND PROCESSING                       │
│                   (ChatContainer.tsx)                               │
└─────────────────────────────────────────────────────────────────────┘
1. User clicks send button
2. handleSendMessage() is triggered
3. Creates/selects conversation in Supabase
4. Saves user message to Supabase
5. Calls cyberSaathiAPI.chat(query)
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 3: API CLIENT REQUEST                       │
│                    (api.js)                                         │
└─────────────────────────────────────────────────────────────────────┘
POST http://127.0.0.1:8000/chat
Headers: { "Content-Type": "application/json" }
Body: { "query": "What are the penalties for hacking under PECA 2016?" }
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 4: FASTAPI ENDPOINT                         │
│                    (api.py - /chat route)                           │
└─────────────────────────────────────────────────────────────────────┘
1. Receives ChatRequest
2. Validates query is not empty
3. Calls run_agent(request.query)
4. Waits for agent response
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  STEP 5: AGENT INITIALIZATION                       │
│                  (agent_graph.py - run_agent)                       │
└─────────────────────────────────────────────────────────────────────┘
1. Creates agent graph with StateGraph
2. Initializes state with query
3. Invokes graph workflow
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               STEP 6: SANITIZATION NODE (Privacy)                   │
│               (agent_graph.py - sanitization_node)                  │
└─────────────────────────────────────────────────────────────────────┘
1. Calls sanitize_query() from privacy/pii_detector.py
2. PIIDetector scans for 10+ types of PII:
   - CNIC: 12345-1234567-1
   - Phone: +92-300-1234567
   - Email: user@example.com
   - Bank accounts, credit cards, IPs, names, addresses, DOB, URLs
3. Redacts detected PII with placeholders:
   - "My CNIC is 12345-1234567-1" → "My CNIC is [REDACTED_CNIC]"
4. Logs redaction event to logs/pii_redactions.log
5. Updates state with:
   - original_query: Original text
   - sanitized_query: Redacted text
   - redaction_info: { redacted: true, count: 1, types: ["CNIC"] }
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STEP 7: ROUTER NODE (Decision)                    │
│                   (agent_graph.py - router_node)                    │
└─────────────────────────────────────────────────────────────────────┘
1. Creates routing prompt for LLM:
   "Analyze this query and determine if it should use:
    - 'law' - for questions about Pakistani cyber laws
    - 'web' - for recent news or current cases"
2. Calls Google Gemini LLM with sanitized query
3. LLM analyzes: "penalties for hacking under PECA 2016"
4. LLM responds: "law"
5. Updates state: source_tool = "law"
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 8A: LAW RETRIEVAL NODE (if law)                   │
│              (agent_graph.py - law_retrieval_node)                  │
└─────────────────────────────────────────────────────────────────────┘
1. Calls get_law_retriever() from tools/law_retriever.py
2. Initializes HuggingFace embeddings (all-MiniLM-L6-v2)
3. Connects to ChromaDB:
   - Collection: pak_cyberlaw_docs
   - Directory: data/chroma_db/
4. Converts query to embedding vector (384 dimensions)
5. Performs similarity search in vector database
6. Retrieves top 10 most relevant document chunks
7. Extracts source document metadata:
   - document_name: "PECA_2016.pdf"
   - document_type: "pdf"
8. Formats context with source citations:
   "[Source 1: PECA_2016.pdf]
    Section 3 - Unauthorized access to information system..."
9. Updates state:
   - context: Formatted document text
   - source_documents: [{ name: "PECA_2016.pdf", type: "pdf" }]
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 8B: WEB SEARCH NODE (if web)                      │
│              (agent_graph.py - web_search_node)                     │
└─────────────────────────────────────────────────────────────────────┘
[Alternative path if router chose "web"]
1. Calls web_search_tool from tools/web_search.py
2. Uses Tavily API to search the web
3. Retrieves recent articles, news, and web pages
4. Formats search results as context
5. Updates state:
   - context: Web search results
   - source_documents: []
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                STEP 9: GENERATION NODE (Answer)                     │
│                (agent_graph.py - generation_node)                   │
└─────────────────────────────────────────────────────────────────────┘
1. Receives state with:
   - sanitized_query: User question (PII-free)
   - context: Retrieved legal documents
   - source_documents: List of sources
   - redaction_info: Privacy metadata

2. Creates system prompt:
   "You are CyberSaathi, an expert on Pakistani cyber laws.
    Provide accurate information, cite specific laws and sections,
    explain in clear language, be professional."

3. Creates user prompt:
   "Based on this context: [Retrieved legal text]
    Answer: What are the penalties for hacking under PECA 2016?"

4. Calls Google Gemini LLM with both prompts

5. LLM generates answer:
   "Under Section 3 of PECA 2016, unauthorized access to an 
    information system is punishable by imprisonment up to 3 years
    or a fine up to Rs. 1 million, or both..."

6. Appends source citations:
   "---
    📚 Sources:
    1. PECA_2016.pdf (PDF)"

7. If PII was redacted, appends privacy notice:
   "---
    🔒 Privacy Notice: For your protection, sensitive personal
    information was automatically detected and removed from your
    query before processing. (1 item(s) redacted)."

8. Updates state:
   - answer: Complete response with citations and privacy notice
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STEP 10: RESPONSE ASSEMBLY                        │
│                   (agent_graph.py - run_agent)                      │
└─────────────────────────────────────────────────────────────────────┘
1. Graph workflow completes
2. Extracts final state
3. Returns dictionary:
   {
     "answer": "Under Section 3 of PECA 2016...\n\n---\n📚 Sources:...",
     "context": "[Source 1: PECA_2016.pdf]\nSection 3...",
     "source_tool": "law",
     "source_documents": [{"name": "PECA_2016.pdf", "type": "pdf"}],
     "pii_redacted": false,
     "redaction_info": {"redacted": false, "count": 0, "types": []}
   }
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STEP 11: API RESPONSE                             │
│                   (api.py - /chat route)                            │
└─────────────────────────────────────────────────────────────────────┘
1. Receives agent result
2. Creates ChatResponse model:
   - answer: Generated answer with citations
   - context: Retrieved context
   - source_tool: "law" or "web"
   - source_documents: List of sources
   - pii_redacted: Boolean
   - redaction_count: Number of items redacted
3. Returns JSON response with 200 OK
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  STEP 12: FRONTEND RECEIVES RESPONSE                │
│                  (api.js - chat method)                             │
└─────────────────────────────────────────────────────────────────────┘
1. Receives JSON response
2. Parses response data
3. Logs: "✅ CyberSaathi response: {...}"
4. Returns data to ChatContainer
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  STEP 13: MESSAGE PERSISTENCE                       │
│                  (ChatContainer.tsx)                                │
└─────────────────────────────────────────────────────────────────────┘
1. Extracts answer from apiResponse.answer
2. Calls saveMessage(conversationId, 'assistant', answer)
3. Saves to Supabase messages table:
   - conversation_id: UUID
   - role: "assistant"
   - content: Full answer with citations
   - created_at: Timestamp
4. Updates conversation updated_at timestamp
5. Adds message to local state
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 14: UI UPDATE                               │
│                    (ChatMessage.tsx)                                │
└─────────────────────────────────────────────────────────────────────┘
1. React re-renders with new message
2. ChatMessage component displays:
   - Avatar with gradient (cyan to orange)
   - Role: "Cyber Law Assistant"
   - Content: Formatted answer with markdown
   - Source citations in styled format
   - Privacy notice if applicable
3. Auto-scrolls to bottom
4. User sees complete response
```

---

### Backend Workflow

#### 1. **API Layer** (`api.py`)
- **FastAPI Application**: Handles HTTP requests
- **CORS Middleware**: Allows cross-origin requests from frontend
- **Endpoints**:
  - `POST /chat`: Main chat endpoint
  - `GET /health`: Health check
  - `GET /info`: API information
- **Request Validation**: Pydantic models ensure data integrity
- **Error Handling**: Comprehensive exception handling with logging

#### 2. **Agent Workflow** (`agent/agent_graph.py`)
The agent uses **LangGraph** to create a stateful workflow with multiple nodes:

**Node 1: Sanitization**
```python
def sanitization_node(state):
    # Detect and redact PII from user query
    sanitized, redaction_info = sanitize_query(original_query)
    # Update state with sanitized query
    state["query"] = sanitized
    state["redaction_info"] = redaction_info
```

**Node 2: Router**
```python
def router_node(state):
    # Use LLM to decide: law database or web search?
    routing_prompt = "Analyze query and respond with 'law' or 'web'"
    response = llm.invoke(routing_prompt)
    state["source_tool"] = response.content  # "law" or "web"
```

**Node 3A: Law Retrieval** (if routed to law)
```python
def law_retrieval_node(state):
    # Retrieve from ChromaDB vector store
    retriever = get_law_retriever()
    documents = retriever.invoke(state["query"])
    # Extract source documents and format context
    state["context"] = formatted_documents
    state["source_documents"] = source_list
```

**Node 3B: Web Search** (if routed to web)
```python
def web_search_node(state):
    # Search web using Tavily API
    context = web_search_tool.invoke(state["query"])
    state["context"] = context
```

**Node 4: Generation**
```python
def generation_node(state):
    # Generate answer using LLM with retrieved context
    system_prompt = "You are CyberSaathi, expert on Pakistani cyber laws"
    user_prompt = f"Context: {state['context']}\nQuestion: {state['query']}"
    answer = llm.invoke([system_prompt, user_prompt])
    # Add source citations and privacy notice
    state["answer"] = answer + citations + privacy_notice
```

#### 3. **Privacy Protection** (`privacy/pii_detector.py`)
- **Pattern Matching**: Regex patterns for 10+ PII types
- **Detection Methods**:
  - `detect_cnic()`: Pakistani CNIC numbers
  - `detect_phone()`: Phone numbers
  - `detect_email()`: Email addresses
  - `detect_bank_account()`: Bank accounts
  - `detect_credit_card()`: Credit cards
  - `detect_ip_address()`: IP addresses
  - `detect_names()`: Personal names
  - `detect_addresses()`: Physical addresses
  - `detect_dob()`: Dates of birth
  - `detect_urls()`: URLs with personal info
- **Redaction**: Replaces PII with placeholders like `[REDACTED_CNIC]`
- **Audit Logging**: Logs all redactions to `logs/pii_redactions.log`

#### 4. **Vector Retrieval** (`tools/law_retriever.py`)
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (384 dimensions)
- **Vector Store**: ChromaDB with persistent storage
- **Similarity Search**: Cosine similarity on embedded vectors
- **Metadata Filtering**: Filter by document type, source, etc.
- **Top-K Retrieval**: Returns 10 most relevant chunks by default

#### 5. **Configuration** (`config.py`)
- **Environment Variables**: Loads from `.env` file
- **Centralized Settings**:
  - API keys (Google, Tavily)
  - Model names (LLM, embeddings)
  - Database paths
  - Retrieval parameters
  - Logging configuration
- **Validation**: Ensures required variables are set

---

### Frontend Workflow

#### 1. **Application Entry** (`main.tsx` → `App.tsx`)
- **Vite**: Fast development server and build tool
- **React 18**: Modern React with hooks
- **State Management**: `useState` for UI state
- **Routing**: Simple conditional rendering (home ↔ chat)

#### 2. **Landing Page**
- **Navigation**: Top bar with logo and "Get Started" button
- **HeroSection**: Eye-catching hero with gradient text and CTA
- **FeatureCards**: Showcase key features with icons
- **Footer**: Legal disclaimer and copyright

#### 3. **Chat Interface** (`ChatContainer.tsx`)
The main chat component orchestrates the entire conversation flow:

**Initialization**
```typescript
useEffect(() => {
  loadConversations();  // Load from Supabase
}, []);
```

**Message Sending**
```typescript
const handleSendMessage = async (content: string) => {
  // 1. Create/select conversation
  let conversationId = currentConversationId || await createNewConversation();
  
  // 2. Save user message to Supabase
  await saveMessage(conversationId, 'user', content);
  
  // 3. Call backend API
  const apiResponse = await cyberSaathiAPI.chat(content);
  
  // 4. Save assistant response to Supabase
  await saveMessage(conversationId, 'assistant', apiResponse.answer);
  
  // 5. Update UI
  setMessages([...messages, userMsg, assistantMsg]);
};
```

#### 4. **API Client** (`components/api.js`)
- **Base URL**: Configurable via `VITE_API_URL` environment variable
- **Methods**:
  - `chat(query)`: Send query to backend
  - `healthCheck()`: Check backend status
  - `getInfo()`: Get API metadata
  - `testConnection()`: Test connectivity
- **Error Handling**: Catches and logs all errors
- **Response Parsing**: Extracts answer from JSON response

#### 5. **Supabase Integration** (`lib/supabase.ts`)
- **Tables**:
  - `conversations`: Stores conversation metadata
  - `messages`: Stores individual messages
- **Operations**:
  - Create conversation
  - Load conversations
  - Save message
  - Load messages
  - Update timestamps
- **Real-time**: Can be extended for real-time updates

#### 6. **Message Display** (`ChatMessage.tsx`)
- **Role-based Styling**: Different colors for user vs assistant
- **Markdown Support**: Can be extended for rich formatting
- **Avatars**: Gradient avatars for visual appeal
- **Timestamps**: Display message creation time

---

## 📦 Installation

### Prerequisites
- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **npm**: 9.0 or higher
- **Git**: For version control

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/CyberSaathi.git
cd CyberSaathi/CyberSaathi_BackEnd
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in `CyberSaathi_BackEnd/`:
```env
# Required API Keys
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# ChromaDB Configuration
CHROMA_COLLECTION_NAME=pak_cyberlaw_docs
CHROMA_PERSIST_DIR=./data/chroma_db

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Retrieval Configuration
RETRIEVAL_K=10
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# LLM Configuration
LLM_MODEL=gemini-2.0-flash-exp
LLM_TEMPERATURE=0

# Logging
LOG_LEVEL=INFO
```

5. **Index documents** (if not already done)
```bash
python index_documents_chromadb.py
```

6. **Start the backend server**
```bash
uvicorn api:api --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../CyberSaathi_FrontEnd
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
Create a `.env` file in `CyberSaathi_FrontEnd/`:
```env
# Backend API URL
VITE_API_URL=http://127.0.0.1:8000

# Supabase Configuration
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

4. **Start the development server**
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

---

## 🚀 Usage

### Starting the Application

1. **Start Backend** (Terminal 1)
```bash
cd CyberSaathi_BackEnd
venv\Scripts\activate  # Windows
uvicorn api:api --reload --host 0.0.0.0 --port 8000
```

2. **Start Frontend** (Terminal 2)
```bash
cd CyberSaathi_FrontEnd
npm run dev
```

3. **Open Browser**
Navigate to `http://localhost:5173`

### Using the Chat Interface

1. Click **"Get Started"** on the landing page
2. Type your question about Pakistani cyber law
3. Press **Enter** or click **Send**
4. View the AI-generated response with source citations
5. Continue the conversation or start a new one

### Example Queries

- "What are the penalties for unauthorized access under PECA 2016?"
- "Explain the definition of cybercrime in Pakistani law"
- "What are my rights if someone hacks my social media account?"
- "Recent cybercrime cases in Pakistan" (triggers web search)
- "How to report a cybercrime in Pakistan?"

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Chat Endpoint
**POST** `/chat`

Send a query and receive an AI-generated response.

**Request Body:**
```json
{
  "query": "What are the penalties for hacking under PECA 2016?"
}
```

**Response:**
```json
{
  "answer": "Under Section 3 of PECA 2016...\n\n---\n📚 Sources:\n1. PECA_2016.pdf (PDF)",
  "context": "[Source 1: PECA_2016.pdf]\nSection 3 - Unauthorized access...",
  "source_tool": "law",
  "source_documents": [
    {
      "name": "PECA_2016.pdf",
      "type": "pdf"
    }
  ],
  "pii_redacted": false,
  "redaction_count": 0
}
```

#### 2. Health Check
**GET** `/health`

Check if the API is operational.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is operational"
}
```

#### 3. API Information
**GET** `/info`

Get information about the API configuration.

**Response:**
```json
{
  "name": "CyberSaathi",
  "description": "Pakistani Cyber Law Chatbot",
  "version": "1.0.0",
  "llm_model": "gemini-2.0-flash-exp",
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "database": "ChromaDB"
}
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🔒 Privacy & Security

### PII Protection

CyberSaathi automatically detects and redacts the following types of Personally Identifiable Information (PII) **before** sending queries to external APIs:

| PII Type | Example | Redacted As |
|----------|---------|-------------|
| CNIC | 12345-1234567-1 | [REDACTED_CNIC] |
| Phone | +92-300-1234567 | [REDACTED_PHONE] |
| Email | user@example.com | [REDACTED_EMAIL] |
| Bank Account | Account: 1234567890 | [REDACTED_ACCOUNT] |
| Credit Card | 1234-5678-9012-3456 | [REDACTED_CARD] |
| IP Address | 192.168.1.1 | [REDACTED_IP] |
| Name | My name is John Doe | My name is [REDACTED_NAME] |
| Address | Living at 123 Main St | Living at [REDACTED_ADDRESS] |
| Date of Birth | DOB: 01/01/1990 | DOB: [REDACTED_DOB] |
| URLs | https://example.com/user/123 | [REDACTED_URL] |

### Privacy Features

- ✅ **Client-Side Detection**: PII never leaves the backend
- ✅ **Automatic Redaction**: No user action required
- ✅ **Audit Logging**: All redactions logged for compliance
- ✅ **User Notification**: Privacy notice shown when PII is detected
- ✅ **No Storage**: Original PII is never stored

### Security Best Practices

- 🔐 **API Keys**: Stored in `.env` files (not committed to Git)
- 🔐 **HTTPS**: Use HTTPS in production
- 🔐 **CORS**: Configure allowed origins in production
- 🔐 **Input Validation**: All inputs validated with Pydantic
- 🔐 **Error Handling**: No sensitive data in error messages

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Issues
- Use GitHub Issues to report bugs
- Include steps to reproduce
- Provide error messages and logs

### Submitting Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write descriptive commit messages
- Add tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the **MY License**.

```
MIT License

Copyright (c) 2024 CyberSaathi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **LangChain**: For the powerful LLM orchestration framework
- **Google Gemini**: For the advanced language model
- **ChromaDB**: For the efficient vector database
- **FastAPI**: For the modern API framework
- **React**: For the excellent UI library
- **Supabase**: For the backend-as-a-service platform

---

## 📞 Contact

For questions, suggestions, or support:

- **GitHub Issues**: [Create an issue](https://github.com/yourusername/CyberSaathi/issues)
- **Email**: huzaifasajidkhokhar@gmail.com

---

## 🗺️ Roadmap

### Upcoming Features
- [ ] Multi-language support (Urdu, English)
- [ ] Voice input/output
- [ ] Document upload for analysis
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Integration with legal databases
- [ ] Real-time collaboration
- [ ] Export chat history (PDF, DOCX)

---

<div align="center">

**Made with ❤️ for the Pakistani legal community**

⭐ **Star this repo if you find it helpful!** ⭐

</div>
