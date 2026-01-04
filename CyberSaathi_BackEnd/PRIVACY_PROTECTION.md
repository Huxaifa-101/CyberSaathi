# 🔒 Privacy Protection Feature - Documentation

## Overview

CyberSaathi now includes **automatic PII (Personally Identifiable Information) detection and redaction** to protect user privacy. When users share their scenarios or personal information, sensitive data is automatically detected and removed **before** being sent to Gemini or any external service.

## 🎯 What Gets Protected

The system automatically detects and redacts:

### Pakistani-Specific PII
- **CNIC Numbers**: 12345-1234567-1 or 1234512345671
- **Phone Numbers**: +92-XXX-XXXXXXX, 03XX-XXXXXXX, etc.

### General PII
- **Email Addresses**: user@example.com
- **Names**: Detected from context ("My name is...", "I am...")
- **Addresses**: Street addresses, cities (Karachi, Lahore, etc.)
- **Bank Account Numbers**: 8-16 digit account numbers
- **Credit Card Numbers**: 13-19 digit card numbers
- **IP Addresses**: XXX.XXX.XXX.XXX
- **URLs**: With potential personal information
- **Date of Birth**: Various formats

## 🔄 How It Works

```
User Query → PII Detection → Redaction → Sanitized Query → LLM Processing
```

### Step-by-Step Process

1. **User submits query** with personal information
2. **PII Detector scans** the query for sensitive data
3. **Redaction** replaces sensitive data with placeholders
4. **Sanitized query** is sent to Gemini and other services
5. **Response generated** based on sanitized query
6. **Privacy notice** added to response if PII was detected

## 📝 Examples

### Example 1: CNIC and Phone Number

**Original Query:**
```
My name is Ahmed Khan, CNIC 12345-1234567-1, phone 0300-1234567. 
Someone hacked my account. What should I do?
```

**Sanitized Query (sent to Gemini):**
```
[REDACTED_NAME], CNIC [REDACTED_CNIC], phone [REDACTED_PHONE]. 
Someone hacked my account. What should I do?
```

**Response:**
```
Based on Pakistani cyber law, if your account was hacked, you should...

---
🔒 Privacy Notice: For your protection, sensitive personal information 
was automatically detected and removed from your query before processing. 
(3 item(s) redacted). Your confidential data was never sent to external services.
```

### Example 2: Email and Address

**Original Query:**
```
I live at House 123, Street 45, Karachi. My email john@example.com 
was used for fraud. What are my legal options?
```

**Sanitized Query:**
```
I live at [REDACTED_ADDRESS]. My email [REDACTED_EMAIL] 
was used for fraud. What are my legal options?
```

### Example 3: No PII

**Original Query:**
```
What are the penalties for unauthorized access under PECA 2016?
```

**Sanitized Query:**
```
What are the penalties for unauthorized access under PECA 2016?
```

**Response:**
```
Under Section 3 of PECA 2016, unauthorized access...
(No privacy notice - no PII detected)
```

## 🔧 Technical Implementation

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Query                              │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Sanitization Node (FIRST STEP)                  │
│                                                              │
│  1. Detect PII using regex patterns                          │
│  2. Redact sensitive data                                    │
│  3. Log redaction event (metadata only)                      │
│  4. Update state with sanitized query                        │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Router Node                               │
│              (Uses sanitized query)                          │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Retrieval / Web Search                          │
│              (Uses sanitized query)                          │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Generation Node                             │
│                                                              │
│  1. Generate answer using sanitized query                    │
│  2. Add privacy notice if PII was redacted                   │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. PII Detector (`privacy/pii_detector.py`)
- Pattern-based detection using regex
- Supports multiple PII types
- Configurable redaction templates

#### 2. Redaction Logger (`privacy/redaction_logger.py`)
- Logs redaction events for audit
- **Does NOT store actual PII values**
- Only stores metadata (type, count, timestamp)

#### 3. Agent Integration (`agent/agent_graph.py`)
- Sanitization as first node in graph
- All downstream nodes use sanitized query
- Privacy notice in final response

## 📊 API Response

The API now includes PII information in responses:

```json
{
  "answer": "Under Section 3 of PECA 2016...\n\n---\n🔒 Privacy Notice: ...",
  "context": "Section 3 - Unauthorized access...",
  "source_tool": "law",
  "pii_redacted": true,
  "redaction_count": 3
}
```

### Response Fields

- **answer**: Generated answer (includes privacy notice if PII detected)
- **context**: Retrieved context
- **source_tool**: "law" or "web"
- **pii_redacted**: Boolean indicating if PII was detected
- **redaction_count**: Number of PII items redacted

## 🧪 Testing

### Run PII Detection Tests

```powershell
python test_pii_detection.py
```

This will test:
- CNIC detection
- Phone number detection
- Email detection
- Name detection
- Multiple PII types
- Real-world scenarios

### Test with API

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "My name is Ahmed, CNIC 12345-1234567-1. What are my rights?"
  }'
```

**Expected Response:**
```json
{
  "answer": "...\n\n---\n🔒 Privacy Notice: For your protection, sensitive personal information was automatically detected and removed from your query before processing. (2 item(s) redacted). Your confidential data was never sent to external services.",
  "pii_redacted": true,
  "redaction_count": 2
}
```

## 📈 Monitoring

### Redaction Logs

Redaction events are logged to `logs/pii_redactions.log`:

```json
{"timestamp": "2026-01-02T16:30:00", "query_id": null, "redaction_count": 2, "types_redacted": ["CNIC", "PHONE"], "redaction_map": {"CNIC": 1, "PHONE": 1}}
```

### View Statistics

```python
from privacy.redaction_logger import RedactionLogger

logger = RedactionLogger(log_file="logs/pii_redactions.log")
stats = logger.get_redaction_stats()

print(f"Total queries with PII: {stats['total_queries_with_pii']}")
print(f"Total redactions: {stats['total_redactions']}")
print(f"By type: {stats['by_type']}")
```

## 🔐 Security Guarantees

### What We Guarantee

✅ **PII never sent to Gemini** - Sanitization happens BEFORE any LLM call
✅ **PII never sent to Tavily** - Web search uses sanitized query
✅ **PII never stored in logs** - Only metadata logged
✅ **Automatic detection** - No user action required
✅ **Transparent** - Users informed when PII is redacted

### What We Log

✅ **Timestamp** of redaction
✅ **Number** of items redacted
✅ **Types** of PII detected (CNIC, PHONE, etc.)
✅ **Query ID** (if provided)

❌ **Actual PII values** - NEVER logged
❌ **Original query** - NEVER logged
❌ **User identity** - NEVER logged

## 🎯 Use Cases

### 1. Cybercrime Reporting
**User:** "I want to report a crime. My CNIC is 12345-1234567-1..."
**System:** Redacts CNIC, processes legal query safely

### 2. Legal Consultation
**User:** "My name is Sara, email sara@example.com. What are my rights?"
**System:** Redacts name and email, provides legal information

### 3. Identity Theft
**User:** "Someone stole my identity. My phone is 0300-1234567..."
**System:** Redacts phone, helps with legal recourse

### 4. General Queries
**User:** "What are the penalties for cyber stalking?"
**System:** No PII detected, processes normally

## ⚙️ Configuration

### Customize Redaction Templates

Edit `privacy/pii_detector.py`:

```python
redaction_templates = {
    "CNIC": "[REDACTED_CNIC]",
    "PHONE": "[REDACTED_PHONE]",
    "EMAIL": "[REDACTED_EMAIL]",
    # Add custom templates
}
```

### Add New PII Types

Add new detection patterns:

```python
# In PIIDetector class
self.custom_pattern = re.compile(r'your_pattern_here')

def detect_custom(self, text: str) -> List[Tuple[str, str]]:
    matches = self.custom_pattern.findall(text)
    return [("CUSTOM_TYPE", match) for match in matches]
```

## 📚 Best Practices

### For Users

1. **Feel safe sharing scenarios** - PII is automatically protected
2. **Check privacy notice** - Confirms what was redacted
3. **Review responses** - Ensure context is maintained

### For Developers

1. **Never bypass sanitization** - Always use the agent pipeline
2. **Monitor redaction logs** - Track PII detection patterns
3. **Test with real data** - Ensure patterns catch all PII types
4. **Update patterns** - Add new PII types as needed

## 🚨 Limitations

### Current Limitations

- **Pattern-based detection** - May miss creative PII formats
- **Context-dependent** - Names only detected with indicators
- **False positives** - Some numbers may be incorrectly flagged
- **Language-specific** - Optimized for English/Urdu romanization

### Future Improvements

- [ ] ML-based PII detection
- [ ] Multi-language support (Urdu script)
- [ ] Custom PII type definitions
- [ ] User-configurable sensitivity levels
- [ ] Advanced name entity recognition

## 🆘 Troubleshooting

### PII Not Detected

**Issue:** Sensitive data not being redacted
**Solution:** 
- Check pattern in `pii_detector.py`
- Add custom detection pattern
- Test with `test_pii_detection.py`

### False Positives

**Issue:** Non-sensitive data being redacted
**Solution:**
- Adjust regex patterns
- Add exclusion rules
- Fine-tune detection thresholds

### Logs Not Created

**Issue:** Redaction logs not appearing
**Solution:**
- Check `logs/` directory exists
- Verify write permissions
- Check `RedactionLogger` initialization

## 📞 Support

For privacy-related questions:
- Review this documentation
- Run `test_pii_detection.py`
- Check `logs/pii_redactions.log`
- Open an issue on GitHub

---

## ✅ Summary

The privacy protection feature ensures that:

1. **All user PII is detected** before processing
2. **Sensitive data never reaches external APIs**
3. **Users are informed** when PII is redacted
4. **Audit trail maintained** without storing actual PII
5. **Zero configuration required** - works automatically

**Your privacy is protected by default! 🔒**
