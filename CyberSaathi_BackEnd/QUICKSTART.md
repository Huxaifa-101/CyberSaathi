# 🚀 Quick Start Guide - CyberSaathi

This guide will help you get CyberSaathi up and running in minutes.

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Google Gemini API key
- [ ] Tavily API key
- [ ] Pakistani cyber law documents (PDFs/DOCX)

**Note:** No database server needed! CyberSaathi uses ChromaDB (file-based).

## 📝 Step-by-Step Setup

### Step 1: Python Environment (3 minutes)

```powershell
# Navigate to project directory
cd C:\Users\mzezo\Desktop\CyberSaathi

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration (2 minutes)

1. **Create `.env` file** in the project root:
   ```env
   # Required API Keys
   GOOGLE_API_KEY=your_gemini_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   
   # Optional (has defaults)
   CHROMA_COLLECTION_NAME=pak_cyberlaw_docs
   CHROMA_PERSIST_DIR=./data/chroma_db
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   RETRIEVAL_K=10
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   LLM_MODEL=gemini-2.0-flash-exp
   LOG_LEVEL=INFO
   ```

2. **Replace the API keys** with your actual values:
   - Get Google Gemini API key from: https://makersuite.google.com/app/apikey
   - Get Tavily API key from: https://tavily.com/

### Step 3: Add Documents (2 minutes)

1. **Place your documents** in `data/raw/` folder:
   - PECA_2016.pdf
   - Cybercrime_Rules_2018.pdf
   - Any other Pakistani cyber law documents

2. **Index the documents**:
   ```powershell
   python index_documents_chromadb.py
   ```

   This will:
   - Load all documents from `data/raw/`
   - Split them into chunks
   - Generate embeddings
   - Store in ChromaDB (file-based, no server needed!)

### Step 4: Start the API (1 minute)

```powershell
uvicorn api:api --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

## 🧪 Test the API

### Option 1: Using Browser
Visit: http://localhost:8000/docs

This opens the interactive Swagger UI where you can test the API.

### Option 2: Using curl

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What are the penalties for unauthorized access under PECA 2016?\"}"
```

### Option 3: Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"query": "What are the penalties for unauthorized access under PECA 2016?"}
)

print(response.json()["answer"])
```

## 🔍 Verify Installation

Check if everything is set up correctly:

```powershell
python verify_installation.py
```

This will check:
- ✅ Python version
- ✅ Required packages
- ✅ API keys
- ✅ ChromaDB setup
- ✅ Indexed documents

## ❓ Troubleshooting

### Issue: "GOOGLE_API_KEY is not set"
**Solution**: Make sure you created the `.env` file and added your API keys

### Issue: "No documents found"
**Solution**: 
- Place PDF/DOCX files in `data/raw/` directory
- Run `python index_documents_chromadb.py`

### Issue: "Module not found"
**Solution**: 
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

### Issue: "ChromaDB error"
**Solution**: 
- Delete `data/chroma_db/` folder
- Re-run `python index_documents_chromadb.py`

## � Connect Your Frontend

### Quick Test
Open `test_frontend.html` in your browser to test the API connection!

### For Your Production Frontend

1. **Update API URL** in your frontend code:
   ```javascript
   const API_URL = 'https://your-ngrok-url.ngrok-free.dev';
   ```

2. **Add Required Header** to skip ngrok warning:
   ```javascript
   headers: {
     'Content-Type': 'application/json',
     'ngrok-skip-browser-warning': 'true'
   }
   ```

3. **Use the API Client** - Copy `cybersaathi-api-client.js` to your frontend project

4. **See Examples**:
   - `test_frontend.html` - Vanilla JavaScript example
   - `CyberSaathiChat.jsx` - React component example
   - `FRONTEND_CONNECTION_GUIDE.md` - Complete guide

### Example API Call
```javascript
const response = await fetch('https://your-ngrok-url.ngrok-free.dev/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true'
  },
  body: JSON.stringify({ query: 'What is PECA 2016?' })
});

const data = await response.json();
console.log(data.answer);
```

## �🎯 Next Steps

1. **Add more documents**: Place more Pakistani cyber law documents in `data/raw/` and run `python index_documents_chromadb.py`

2. **Customize the chatbot**: Edit prompts in `agent/agent_graph.py` to customize behavior

3. **Connect your frontend**: See `FRONTEND_CONNECTION_GUIDE.md` for detailed instructions

4. **Deploy**: Deploy to a cloud platform (AWS, Azure, Google Cloud)

## 📚 Useful Commands

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Start API
uvicorn api:api --reload --host 0.0.0.0 --port 8000

# Index documents
python index_documents_chromadb.py

# Force re-index all documents
python index_documents_chromadb.py --force

# Verify installation
python verify_installation.py

# Show architecture
python show_architecture.py

# Deactivate virtual environment
deactivate
```

## 🆘 Getting Help

- Check the main README.md for detailed documentation
- Review CHROMADB_MIGRATION.md for database details
- Check show_architecture.py for system architecture

---

**Ready to go! 🚀**

Your CyberSaathi chatbot is now ready to answer questions about Pakistani cyber laws!

## 💡 Why ChromaDB?

- ✅ **No database server needed** - Just files on disk
- ✅ **Easy setup** - No PostgreSQL installation
- ✅ **Portable** - Copy the `data/` folder to move your database
- ✅ **Fast** - Optimized for vector similarity search
- ✅ **Perfect for development** - Simple and effective
