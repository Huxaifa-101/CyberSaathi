# 🔗 Connecting Bolt.new Frontend to CyberSaathi Backend

## Your Setup
- **Frontend (Bolt.new)**: https://cybersaathi-ai.bolt.host/
- **Backend (FastAPI)**: https://unesoteric-autumn-nonintermittently.ngrok-free.dev/
- **Framework**: Vite + React (based on your environment variables)

## 📋 Step-by-Step Instructions

### Step 1: Access Your Bolt.new Project

1. Go to https://bolt.new
2. Open your CyberSaathi project
3. You should see your project files in the editor

### Step 2: Create Environment Variable File

In your Bolt.new project, create or update `.env` file:

```env
# Existing Supabase config
VITE_SUPABASE_URL=https://ijixfqzqorajidjvqrym.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlqaXhmcXpxb3JhamlkanZxcnltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcyODUxNTAsImV4cCI6MjA4Mjg2MTE1MH0.jXAZS6NUM6who6Ou46sr4e65QchWVYpxXXYQTxuOu6I

# Add this for your CyberSaathi backend
VITE_API_URL=https://unesoteric-autumn-nonintermittently.ngrok-free.dev
```

### Step 3: Create API Configuration File

Create a new file `src/config/api.js` (or `src/config/api.ts` if using TypeScript):

```javascript
// src/config/api.js
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://unesoteric-autumn-nonintermittently.ngrok-free.dev';

export const apiConfig = {
  baseUrl: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true'
  }
};

// API Client
export const cyberSaathiAPI = {
  async chat(query) {
    const response = await fetch(`${apiConfig.baseUrl}/chat`, {
      method: 'POST',
      headers: apiConfig.headers,
      body: JSON.stringify({ query })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  },

  async healthCheck() {
    const response = await fetch(`${apiConfig.baseUrl}/health`, {
      headers: apiConfig.headers
    });
    return response.json();
  },

  async getInfo() {
    const response = await fetch(`${apiConfig.baseUrl}/info`, {
      headers: apiConfig.headers
    });
    return response.json();
  }
};
```

### Step 4: Update Your Chat Component

Find your chat component (likely in `src/components/` or `src/pages/`) and update it:

**Before (probably looks like this):**
```javascript
// ❌ Old code - won't work
const handleSubmit = async (question) => {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: question })
  });
  const data = await response.json();
  // ...
};
```

**After (update to this):**
```javascript
// ✅ New code - will work!
import { cyberSaathiAPI } from '../config/api';

const handleSubmit = async (question) => {
  try {
    const data = await cyberSaathiAPI.chat(question);
    console.log('Answer:', data.answer);
    console.log('Sources:', data.source_documents);
    // Update your UI with the response
    setAnswer(data.answer);
    setSources(data.source_documents);
  } catch (error) {
    console.error('Error:', error);
    setError(error.message);
  }
};
```

### Step 5: Example Complete React Component

Here's a complete example of how your chat component should look:

```jsx
import React, { useState, useEffect } from 'react';
import { cyberSaathiAPI } from '../config/api';

function ChatComponent() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [connected, setConnected] = useState(false);

  // Check connection on mount
  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      await cyberSaathiAPI.healthCheck();
      setConnected(true);
      console.log('✅ Connected to CyberSaathi backend');
    } catch (err) {
      setConnected(false);
      console.error('❌ Cannot connect to backend:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await cyberSaathiAPI.chat(question);
      setAnswer(data.answer);
      setSources(data.source_documents || []);
    } catch (err) {
      setError(err.message);
      console.error('Chat error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      {/* Connection Status */}
      <div className={`status ${connected ? 'connected' : 'disconnected'}`}>
        {connected ? '🟢 Connected' : '🔴 Disconnected'}
      </div>

      {/* Chat Form */}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about Pakistani cyber law..."
          disabled={!connected || loading}
        />
        <button type="submit" disabled={!connected || loading}>
          {loading ? 'Loading...' : 'Ask'}
        </button>
      </form>

      {/* Error Display */}
      {error && (
        <div className="error">
          ❌ Error: {error}
        </div>
      )}

      {/* Answer Display */}
      {answer && (
        <div className="answer">
          <h3>Answer:</h3>
          <p>{answer}</p>
          
          {sources.length > 0 && (
            <div className="sources">
              <h4>📚 Sources:</h4>
              {sources.map((source, idx) => (
                <div key={idx}>
                  {idx + 1}. {source.name} ({source.type})
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ChatComponent;
```

## 🔍 How to Find Your Chat Component in Bolt.new

Look for files with names like:
- `Chat.jsx` or `Chat.tsx`
- `ChatBot.jsx` or `ChatBot.tsx`
- `App.jsx` or `App.tsx`
- `index.jsx` or `index.tsx`
- Any file in `src/components/` or `src/pages/`

Search for keywords:
- `fetch(`
- `axios.post(`
- `chat`
- `query`
- `localhost:8000`

## 🧪 Testing in Bolt.new

After making changes:

1. **Save the files** in Bolt.new
2. **Bolt.new will auto-reload** your site
3. **Open browser console** (F12) on your site
4. **Check for connection message**: Should see "✅ Connected to CyberSaathi backend"
5. **Try asking a question**

## 🚨 Common Issues in Bolt.new

### Issue 1: Environment Variables Not Loading
**Solution**: 
- Make sure `.env` file is in the root directory
- Restart the Bolt.new preview
- Variables must start with `VITE_`

### Issue 2: CORS Error
**Solution**: Already fixed! Your backend has CORS enabled.

### Issue 3: Module Not Found
**Solution**: Make sure the import path is correct:
```javascript
import { cyberSaathiAPI } from './config/api';  // Adjust path as needed
```

### Issue 4: Still Using Localhost
**Solution**: 
- Clear browser cache
- Hard refresh (Ctrl + Shift + R)
- Check console for the actual URL being called

## 📝 Quick Checklist for Bolt.new

- [ ] Add `VITE_API_URL` to `.env` file
- [ ] Create `src/config/api.js` with the API client
- [ ] Find your chat component
- [ ] Import and use `cyberSaathiAPI.chat()`
- [ ] Add error handling
- [ ] Test the connection
- [ ] Check browser console for errors

## 🎯 What to Look For in Your Existing Code

Search your Bolt.new project for these patterns and replace them:

### Pattern 1: Direct fetch calls
```javascript
// ❌ Find this
fetch('http://localhost:8000/chat', ...)

// ✅ Replace with this
import { cyberSaathiAPI } from './config/api';
cyberSaathiAPI.chat(question)
```

### Pattern 2: Axios calls
```javascript
// ❌ Find this
axios.post('http://localhost:8000/chat', ...)

// ✅ Replace with this
import { cyberSaathiAPI } from './config/api';
cyberSaathiAPI.chat(question)
```

### Pattern 3: Hardcoded URLs
```javascript
// ❌ Find this
const API_URL = 'http://localhost:8000';

// ✅ Replace with this
const API_URL = import.meta.env.VITE_API_URL;
```

## 💡 Pro Tips for Bolt.new

1. **Use Environment Variables**: Always use `import.meta.env.VITE_API_URL`
2. **Check Console**: Open browser console to see connection status
3. **Test Incrementally**: First test health check, then chat
4. **Keep Ngrok Running**: Your backend must be running for this to work

## 🆘 Need Help?

If you're stuck, share:
1. Your chat component code from Bolt.new
2. Any error messages from browser console
3. Screenshot of your Bolt.new file structure

---

**Remember**: Every time you restart ngrok, the URL changes! Update your `.env` file when that happens.
