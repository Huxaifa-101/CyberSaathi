# 🚀 QUICK START: Connect Bolt.new to Your Backend

## ⚡ 3-Step Process

### Step 1️⃣: Add Environment Variable

In your **Bolt.new project**, create/update `.env` file:

```env
VITE_API_URL=https://unesoteric-autumn-nonintermittently.ngrok-free.dev
```

---

### Step 2️⃣: Add API Client

Create a new file: `src/config/api.js`

Copy the entire content from: **`bolt-api-client.js`** (in this folder)

---

### Step 3️⃣: Update Your Chat Component

Find your chat component and update it:

**FIND THIS:**
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  body: JSON.stringify({ query: question })
});
```

**REPLACE WITH THIS:**
```javascript
import { cyberSaathiAPI } from './config/api';

// In your function:
const data = await cyberSaathiAPI.chat(question);
console.log(data.answer);
```

---

## ✅ That's It!

Your Bolt.new site will now connect to your FastAPI backend!

---

## 🧪 Test It

1. Save changes in Bolt.new
2. Open your site: https://cybersaathi-ai.bolt.host/
3. Open browser console (F12)
4. Look for: `✅ CyberSaathi API URL: https://...`
5. Ask a question!

---

## 🆘 Troubleshooting

**Not working?** Check:
- [ ] `.env` file has `VITE_API_URL`
- [ ] You imported `cyberSaathiAPI` in your component
- [ ] Your backend is running (visit the /docs URL)
- [ ] Browser console shows no errors

---

## 📁 Files You Need

1. **`bolt-api-client.js`** → Copy to `src/config/api.js` in Bolt.new
2. **`BOLT_INTEGRATION_GUIDE.md`** → Full detailed guide

---

## 💡 Example Usage

```javascript
import { cyberSaathiAPI } from './config/api';

// Ask a question
const response = await cyberSaathiAPI.chat('What is PECA 2016?');
console.log(response.answer);
console.log(response.source_documents);

// Check connection
const isConnected = await cyberSaathiAPI.testConnection();
console.log('Connected:', isConnected);
```

---

**Need more help?** Read `BOLT_INTEGRATION_GUIDE.md` for detailed instructions!
