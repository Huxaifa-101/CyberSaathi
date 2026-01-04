# 🇵🇰 CyberSaathi - Pakistani Cyber Law Chatbot

A RAG-based (Retrieval-Augmented Generation) chatbot for Pakistani cybercrime laws and regulations, powered by LangChain, PostgreSQL with pgvector, and Google Gemini.

## 🌟 Features

- **🔒 Privacy Protection**: Automatic PII detection and redaction before sending to LLM
- **📚 Source Citations**: Every answer includes references to the law documents used
- **Intelligent Routing**: Automatically routes queries to law database or web search
- **Vector Search**: Fast semantic search using PostgreSQL with pgvector extension
- **Document Management**: Easy upload, update, and deletion of law documents
- **RESTful API**: FastAPI-based API for easy integration
- **Multi-format Support**: Handles PDF, DOCX, and TXT documents
- **Deduplication**: Automatic detection of unchanged documents
- **Metadata Filtering**: Advanced search with document-specific filters

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+ with pgvector extension
- Google Gemini API key
- Tavily API key (for web search)

## 🚀 Quick Start

### 1. PostgreSQL Setup

```powershell
# Install PostgreSQL if not already installed
# Download from: https://www.postgresql.org/download/

# Install pgvector extension
# Download from: https://github.com/pgvector/pgvector

# Create database and run setup script
psql -U postgres
CREATE DATABASE pak_cyberlaw_db;
\c pak_cyberlaw_db
\i setup_postgres.sql
```

### 2. Python Environment

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file (copy from `.env.example`):

```env
# API Keys
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pak_cyberlaw_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here

# Other settings (defaults are fine)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
RETRIEVAL_K=10
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
LLM_MODEL=gemini-2.0-flash-exp
LLM_TEMPERATURE=0
LOG_LEVEL=INFO
```

### 4. Index Documents

```powershell
# Place your cyber law PDFs/DOCX files in data/raw/
# Then run the indexing script
python index_documents.py

# Force re-index all documents
python index_documents.py --force
```

### 5. Start the API

```powershell
uvicorn api:api --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 Source Citations

Every answer from the law database includes citations showing which documents were used.

### Example Response

```
Under Section 3 of PECA 2016, unauthorized access to a computer 
system is punishable by imprisonment up to 3 years or a fine up 
to Rs. 500,000, or both.

---
📚 Sources:
1. Electronic Crimes Act - 2016.pdf (PDF)
2. PECA_2016_Sample.txt (TXT)
```

### API Response

```json
{
  "answer": "Legal answer with citations...",
  "source_documents": [
    {"name": "Electronic Crimes Act - 2016.pdf", "type": "pdf"}
  ],
  "source_tool": "law"
}
```

For detailed documentation, see [SOURCE_CITATIONS.md](SOURCE_CITATIONS.md)

## 🔒 Privacy Protection

CyberSaathi automatically detects and redacts PII (Personally Identifiable Information) before sending queries to external services.

### Protected Information

- Pakistani CNIC numbers
- Phone numbers
- Email addresses
- Names (from context)
- Addresses
- Bank account numbers
- And more...

### Example

**User Query:**
```
My name is Ahmed, CNIC 12345-1234567-1. What are my rights?
```

**Sanitized Query (sent to Gemini):**
```
[REDACTED_NAME], CNIC [REDACTED_CNIC]. What are my rights?
```

**Response includes privacy notice:**
```
🔒 Privacy Notice: For your protection, sensitive personal information 
was automatically detected and removed from your query before processing. 
(2 item(s) redacted).
```

### Test Privacy Protection

```powershell
python test_pii_detection.py
```

For detailed documentation, see [PRIVACY_PROTECTION.md](PRIVACY_PROTECTION.md)

## 📚 Usage

### API Endpoints

#### Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the penalties for unauthorized access under PECA 2016?"
  }'
```

**Response:**
```json
{
  "answer": "Under Section 3 of PECA 2016, unauthorized access to a computer system is punishable by imprisonment up to 3 years or a fine up to Rs. 500,000, or both.",
  "context": "Section 3 - Unauthorized access to information system...",
  "source_tool": "law"
}
```

#### Health Check

```bash
curl http://localhost:8000/health
```

#### API Info

```bash
curl http://localhost:8000/info
```

### Document Management

```powershell
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
```

### Test Retrieval

```powershell
python retriever_test.py
```

## 🏗️ Project Structure

```
CyberSaathi/
├── .env                          # Environment variables (create from .env.example)
├── .env.example                  # Template for environment variables
├── .gitignore                    # Git ignore file
├── requirements.txt              # Python dependencies
├── config.py                     # Centralized configuration
├── api.py                        # FastAPI REST endpoint
├── index_documents.py            # Bulk document indexing
├── manage_documents.py           # Document management CLI
├── retriever_test.py             # Test retrieval functionality
├── setup_postgres.sql            # Database schema
├── README.md                     # This file
├── Implementation Plan.text      # Detailed implementation plan
├── data/
│   ├── raw/                      # Upload PDFs/DOCX here
│   └── processed/                # Metadata tracking
├── agent/
│   ├── __init__.py
│   └── agent_graph.py           # LangGraph routing logic
└── tools/
    ├── __init__.py
    ├── law_retriever.py         # PostgreSQL vector retrieval
    └── web_search.py            # Tavily web search
```

## 🔧 Advanced Features

### Metadata Filtering

```python
from tools.law_retriever import search_with_filter

# Search only in specific document
results = search_with_filter(
    query="penalties",
    filters={"document_name": "PECA_2016.pdf"},
    k=5
)

# Search by custom metadata
results = search_with_filter(
    query="data protection",
    filters={"metadata.category": "privacy"},
    k=5
)
```

### Database Queries

```sql
-- Check document count
SELECT COUNT(*) FROM law_documents;

-- View document statistics
SELECT * FROM document_stats;

-- Check storage size
SELECT pg_size_pretty(pg_total_relation_size('law_documents'));

-- Find documents needing update
SELECT * FROM document_registry 
WHERE last_updated < NOW() - INTERVAL '30 days';
```

## 📊 Database Schema

### law_documents Table
Stores chunked documents with embeddings

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| document_name | VARCHAR(500) | Source document name |
| document_type | VARCHAR(50) | pdf, docx, txt |
| chunk_text | TEXT | Actual text chunk |
| chunk_index | INTEGER | Position in document |
| metadata | JSONB | Custom metadata |
| embedding | vector(384) | Vector embedding |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### document_registry Table
Tracks uploaded documents

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| document_name | VARCHAR(500) | Unique document name |
| file_path | TEXT | Path to original file |
| file_hash | VARCHAR(64) | SHA-256 hash for change detection |
| document_type | VARCHAR(50) | File type |
| total_chunks | INTEGER | Number of chunks created |
| upload_date | TIMESTAMP | First upload |
| last_updated | TIMESTAMP | Last modification |
| status | VARCHAR(50) | active, archived, deleted |
| metadata | JSONB | Custom metadata |

## 🎯 Sample Documents to Include

1. **PECA 2016** - Prevention of Electronic Crimes Act
2. **Cybercrime Rules 2018**
3. **Data Protection Act** (if applicable)
4. **IT Policy Documents**
5. **Case Law Summaries**
6. **FIA Cybercrime Guidelines**
7. **SECP Regulations**
8. **PTA Regulations**

## 🔍 How It Works

1. **User Query** → Received by FastAPI endpoint
2. **Router** → LLM classifies query as "law" or "web"
3. **Retrieval** → 
   - **Law**: PostgreSQL vector search retrieves relevant law chunks
   - **Web**: Tavily searches the web for current information
4. **Generation** → Gemini generates answer based on retrieved context
5. **Response** → Formatted answer with sources returned to user

## 🛠️ Maintenance

### Performance Optimization

```sql
-- Vacuum and analyze
VACUUM ANALYZE law_documents;

-- Rebuild index
REINDEX INDEX law_documents_embedding_idx;
```

### Backup

```powershell
# Backup database
pg_dump -U postgres pak_cyberlaw_db > backup.sql

# Restore database
psql -U postgres pak_cyberlaw_db < backup.sql
```

## 📝 API Documentation

Once the API is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Vector search by [pgvector](https://github.com/pgvector/pgvector)
- Web search by [Tavily](https://tavily.com/)

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for Pakistan's digital safety**
