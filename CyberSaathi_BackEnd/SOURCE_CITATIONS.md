# 📚 Source Citations Feature - Documentation

## Overview

CyberSaathi now automatically includes **source document citations** in responses, showing users exactly which Pakistani cyber law documents were used to answer their questions. This adds transparency, credibility, and allows users to verify information.

## 🎯 What's Included

### In Every Response (when using law database)

1. **Answer** - The generated legal advice
2. **Source Citations** - List of documents used
3. **Privacy Notice** - If PII was redacted (optional)

### Example Response

```
Under Section 3 of the Prevention of Electronic Crimes Act 2016, 
unauthorized access to an information system is punishable by:
- Imprisonment up to 3 years, OR
- Fine up to Rs. 500,000, OR
- Both

The offense is committed when someone intentionally accesses a system 
without authorization or exceeds their authorized access with intent 
to cause damage.

---
📚 Sources:
1. Electronic Crimes Act - 2016.pdf (PDF)
2. PECA_2016_Sample.txt (TXT)

---
🔒 Privacy Notice: For your protection, sensitive personal information 
was automatically detected and removed from your query before processing. 
(1 item(s) redacted).
```

## 📊 API Response Structure

### New Field: `source_documents`

```json
{
  "answer": "Legal answer with citations...",
  "context": "Retrieved context...",
  "source_tool": "law",
  "source_documents": [
    {
      "name": "Electronic Crimes Act - 2016.pdf",
      "type": "pdf"
    },
    {
      "name": "Pakistan Penal Code Act - 1860.pdf",
      "type": "pdf"
    }
  ],
  "pii_redacted": false,
  "redaction_count": 0
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | Generated answer with inline citations |
| `context` | string | Retrieved context from documents |
| `source_tool` | string | "law" or "web" |
| `source_documents` | array | List of source documents (only for "law") |
| `pii_redacted` | boolean | Whether PII was detected |
| `redaction_count` | integer | Number of PII items redacted |

## 🔍 How It Works

### 1. Query Processing

```
User Query → Sanitization → Router → Law Retrieval
```

### 2. Document Retrieval

```python
# System retrieves relevant chunks from multiple documents
documents = [
    {
        "content": "Section 3 - Unauthorized access...",
        "metadata": {
            "document_name": "Electronic Crimes Act - 2016.pdf",
            "document_type": "pdf",
            "chunk_index": 5
        }
    },
    {
        "content": "Section 7 - Cyber stalking...",
        "metadata": {
            "document_name": "PECA_2016_Sample.txt",
            "document_type": "txt",
            "chunk_index": 12
        }
    }
]
```

### 3. Source Extraction

```python
# System extracts unique document names
source_documents = [
    {"name": "Electronic Crimes Act - 2016.pdf", "type": "pdf"},
    {"name": "PECA_2016_Sample.txt", "type": "txt"}
]
```

### 4. Citation Formatting

```python
# System appends citations to answer
citations = """
---
📚 Sources:
1. Electronic Crimes Act - 2016.pdf (PDF)
2. PECA_2016_Sample.txt (TXT)
"""
```

## 📝 Examples

### Example 1: Single Source

**Query:**
```
What are the penalties for unauthorized access?
```

**Response:**
```
Under Section 3 of PECA 2016, unauthorized access to a computer 
system is punishable by imprisonment up to 3 years or a fine up 
to Rs. 500,000, or both.

---
📚 Sources:
1. Electronic Crimes Act - 2016.pdf (PDF)
```

### Example 2: Multiple Sources

**Query:**
```
What laws cover cybercrime in Pakistan?
```

**Response:**
```
Pakistani cybercrime is primarily governed by:

1. Prevention of Electronic Crimes Act (PECA) 2016
2. Pakistan Penal Code 1860 (relevant sections)
3. Electronic Transactions Ordinance 2002
4. Telecommunication Act 1996

These laws cover various aspects including unauthorized access, 
data theft, cyber stalking, and electronic fraud.

---
📚 Sources:
1. Electronic Crimes Act - 2016.pdf (PDF)
2. Pakistan Penal Code Act - 1860.pdf (PDF)
3. Electronic Funds Transfer Act - 2007.pdf (PDF)
4. Telecommunication Act - 1996.pdf (PDF)
```

### Example 3: Web Search (No Citations)

**Query:**
```
Recent cybercrime cases in Pakistan 2026
```

**Response:**
```
Based on recent web sources, here are some notable cybercrime 
cases in Pakistan in 2026...

(No source citations - web search results include URLs in context)
```

## 🎨 Citation Format

### In Answer Text

```markdown
---
📚 Sources:
1. Document_Name.pdf (PDF)
2. Another_Document.docx (DOCX)
3. Third_Document.txt (TXT)
```

### In API Response

```json
"source_documents": [
  {"name": "Document_Name.pdf", "type": "pdf"},
  {"name": "Another_Document.docx", "type": "docx"},
  {"name": "Third_Document.txt", "type": "txt"}
]
```

## 🔧 Technical Implementation

### Agent Graph Changes

```python
# In law_retrieval_node
def law_retrieval_node(state: AgentState) -> AgentState:
    # Retrieve documents
    documents = retriever.invoke(query)
    
    # Extract unique source documents
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
    
    # Store in state
    state["source_documents"] = source_docs
    return state
```

### Generation Node Changes

```python
# In generation_node
def generation_node(state: AgentState) -> AgentState:
    # Generate answer
    answer = llm.invoke(...)
    
    # Add source citations if from law documents
    if source_tool == "law" and source_documents:
        citations = "\n\n---\n**📚 Sources:**\n"
        for i, doc in enumerate(source_documents, 1):
            doc_name = doc['name']
            doc_type = doc.get('type', 'unknown').upper()
            citations += f"{i}. {doc_name} ({doc_type})\n"
        answer = answer + citations
    
    return state
```

## 📊 Benefits

### For Users

✅ **Transparency** - Know exactly which laws were referenced  
✅ **Verification** - Can look up original documents  
✅ **Trust** - See that answers are based on real legal documents  
✅ **Learning** - Understand which laws apply to their situation  

### For Legal Professionals

✅ **Citation tracking** - Easy to reference source materials  
✅ **Credibility** - Responses backed by official documents  
✅ **Audit trail** - Know which documents were consulted  
✅ **Research** - Identify relevant laws quickly  

### For Developers

✅ **Debugging** - See which documents are being retrieved  
✅ **Quality control** - Verify correct documents are used  
✅ **Analytics** - Track which documents are most useful  
✅ **Compliance** - Demonstrate proper attribution  

## 🧪 Testing

### Test with API

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the penalties for cyber stalking?"
  }'
```

### Expected Response

```json
{
  "answer": "Under Section 7 of PECA 2016...\n\n---\n📚 Sources:\n1. Electronic Crimes Act - 2016.pdf (PDF)",
  "context": "...",
  "source_tool": "law",
  "source_documents": [
    {
      "name": "Electronic Crimes Act - 2016.pdf",
      "type": "pdf"
    }
  ],
  "pii_redacted": false,
  "redaction_count": 0
}
```

## 📈 Analytics

### Track Source Usage

You can analyze which documents are most frequently used:

```python
from collections import Counter

# Collect source documents from multiple queries
all_sources = []
for response in responses:
    all_sources.extend([doc['name'] for doc in response['source_documents']])

# Count frequency
source_frequency = Counter(all_sources)

print("Most referenced documents:")
for doc, count in source_frequency.most_common(5):
    print(f"{doc}: {count} times")
```

**Example Output:**
```
Most referenced documents:
Electronic Crimes Act - 2016.pdf: 145 times
Pakistan Penal Code Act - 1860.pdf: 89 times
Telecommunication Act - 1996.pdf: 67 times
Personal Data Protection Act - 2017.pdf: 45 times
Criminal Laws Act - 2023.pdf: 34 times
```

## 🎯 Use Cases

### 1. Legal Research

**Scenario:** Lawyer researching cyber stalking laws  
**Benefit:** Immediately see which acts contain relevant provisions  
**Action:** Can reference specific documents in legal briefs  

### 2. Citizen Inquiry

**Scenario:** Citizen asking about their rights  
**Benefit:** Know which laws protect them  
**Action:** Can request full documents from authorities  

### 3. Academic Study

**Scenario:** Student studying Pakistani cyber law  
**Benefit:** Identify primary sources for research  
**Action:** Can cite specific acts in papers  

### 4. Compliance Check

**Scenario:** Business checking compliance requirements  
**Benefit:** See all applicable regulations  
**Action:** Can review full documents for compliance  

## 🔄 Integration with Other Features

### Works Seamlessly With:

1. **PII Protection** - Citations added after privacy notice
2. **Web Search** - Only shows for law database queries
3. **Multi-document Retrieval** - Deduplicates source list
4. **Context Formatting** - Each chunk labeled with source

### Response Structure

```
[Answer]

---
📚 Sources:
[Source citations]

---
🔒 Privacy Notice:
[Privacy notice if applicable]
```

## 📚 Best Practices

### For Users

1. **Verify important information** - Check original documents for critical decisions
2. **Note document names** - Keep track of relevant laws
3. **Request full documents** - If you need complete text

### For Developers

1. **Monitor source quality** - Ensure correct documents are indexed
2. **Track citation patterns** - Identify gaps in document coverage
3. **Update documents regularly** - Keep law database current
4. **Validate metadata** - Ensure document names are accurate

## 🆘 Troubleshooting

### No Sources Shown

**Issue:** Response doesn't include source citations  
**Possible Causes:**
- Query routed to web search (not law database)
- No documents retrieved
- Error in retrieval

**Solution:**
- Check `source_tool` field (should be "law")
- Verify documents are indexed
- Check retrieval logs

### Wrong Documents Cited

**Issue:** Citations don't match answer content  
**Possible Causes:**
- Incorrect metadata in database
- Document name mismatch

**Solution:**
- Re-index documents
- Verify document names in database
- Check metadata in `document_registry` table

## ✅ Summary

The source citations feature provides:

1. **Transparency** - Users see which documents were used
2. **Credibility** - Answers backed by official sources
3. **Traceability** - Easy to verify information
4. **Compliance** - Proper attribution of legal sources

**Every law-based answer now includes clear citations! 📚**

---

*For more information, see the main README.md*
