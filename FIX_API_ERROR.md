# 🔧 Quick Fix: Agent Zero API Error

## The Error You're Seeing

```
AuthenticationError: OpenrouterException - {"error":{"message":"No cookie auth credentials found","code":401}}
```

## ✅ Quick Solution (2 minutes)

### Step 1: Get OpenRouter API Key (Free)

1. Go to: **https://openrouter.ai/keys**
2. Sign up (free) - use Google/GitHub for fastest signup
3. Click **"Create Key"**
4. Copy the key (starts with `sk-or-v1-...`)

### Step 2: Add Key to Agent Zero

1. Open Agent Zero: **http://localhost:50001**
2. Click **Settings** icon (⚙️) in the top right
3. Find **"API Keys"** or **"Secrets"** section
4. Paste your OpenRouter API key
5. Click **Save**

### Step 3: Test

Send a message - the error should be gone! ✅

---

## Alternative: Use Free Model

In Settings, you can also select a **free model**:
- `meta-llama/llama-3.2-3b-instruct:free`
- Or other free models listed in OpenRouter

---

## Need More Help?

See **`AGENT_ZERO_API_SETUP.md`** for:
- Detailed step-by-step instructions
- Other provider options (Google AI, OpenAI, etc.)
- Troubleshooting tips
- Free tier information

---

**That's it! Once you add the API key, Agent Zero will work perfectly.** 🚀

