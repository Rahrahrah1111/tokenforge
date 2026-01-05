# Agent Zero API Key Configuration Guide

## The Problem

You're seeing this error:
```
AuthenticationError: OpenrouterException - {"error":{"message":"No cookie auth credentials found","code":401}}
```

This means Agent Zero needs an API key to use the LLM (Language Model) service.

---

## Quick Fix: Configure API Key in Agent Zero

### Option 1: OpenRouter API Key (Recommended - Free Tier Available)

1. **Get an OpenRouter API Key:**
   - Go to: https://openrouter.ai/
   - Click "Sign In" or "Get Started"
   - Sign up with your email (or use Google/GitHub)
   - Go to: https://openrouter.ai/keys
   - Click "Create Key"
   - Copy your API key

2. **Add the Key in Agent Zero:**
   - In Agent Zero web UI (http://localhost:50001)
   - Click the **Settings** icon (⚙️) in the top right
   - Find the **API Keys** or **Secrets** section
   - Add your OpenRouter API key
   - Save settings

3. **Test:**
   - Try sending a message again
   - The error should be gone!

---

### Option 2: Use Another LLM Provider

Agent Zero supports many providers. In Settings, you can configure:

- **OpenAI** - Requires OpenAI API key
- **Google AI (Gemini)** - Free tier available
- **Anthropic (Claude)** - Requires API key
- **Local Models** - If you have Ollama or similar running
- **Other providers** - Check Agent Zero settings for full list

---

## Step-by-Step: OpenRouter Setup

### Step 1: Create OpenRouter Account

1. Visit: https://openrouter.ai/
2. Click "Sign In" or "Get Started"
3. Sign up with:
   - Email + Password, OR
   - Google account, OR
   - GitHub account

### Step 2: Get Your API Key

1. After signing in, go to: https://openrouter.ai/keys
2. Click **"Create Key"**
3. Give it a name (e.g., "Agent Zero")
4. Copy the key (it will look like: `sk-or-v1-...`)

### Step 3: Add Key to Agent Zero

1. Open Agent Zero: http://localhost:50001
2. Click the **Settings** icon (⚙️) - usually in top right corner
3. Look for:
   - **"API Keys"** section, OR
   - **"Secrets"** section, OR
   - **"LLM Provider"** settings
4. Find **OpenRouter** or **OpenRouter API Key** field
5. Paste your API key
6. Click **Save** or **Apply**

### Step 4: Select Model

In Settings, you may also need to:
- Select a model (e.g., "gpt-3.5-turbo", "gpt-4", "claude-3-haiku")
- OpenRouter offers many models, including free ones

### Step 5: Test

Send a message like "hello" and it should work!

---

## Alternative: Environment Variable (Advanced)

If you want to set the API key via environment variable:

1. **Stop Agent Zero:**
   ```bash
   bash stop_agent_zero.sh
   ```

2. **Edit docker-compose.agent-zero.yml:**
   Add to the environment section:
   ```yaml
   environment:
     - OPENROUTER_API_KEY=your-key-here
   ```

3. **Restart:**
   ```bash
   bash start_agent_zero.sh
   ```

---

## Free Options

### OpenRouter Free Tier
- Some models are free (with rate limits)
- Check: https://openrouter.ai/models for free models
- Examples: "meta-llama/llama-3.2-3b-instruct:free"

### Google AI (Gemini) - Free
1. Go to: https://aistudio.google.com/app/apikey
2. Create API key (free)
3. In Agent Zero Settings, switch provider to "Google AI"
4. Add your Google API key

### Local Models (Ollama)
If you have Ollama running locally:
1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3`
3. In Agent Zero Settings, configure local model endpoint

---

## Troubleshooting

### "Still getting 401 error"
- ✅ Make sure you saved the settings
- ✅ Refresh the page after saving
- ✅ Check that the key is correct (no extra spaces)
- ✅ Verify the key works at https://openrouter.ai/keys

### "Can't find Settings"
- Look for ⚙️ icon in the UI
- Check the top menu bar
- Try clicking your profile/account icon
- Settings might be in a sidebar menu

### "Key format looks wrong"
- OpenRouter keys start with: `sk-or-v1-...`
- Make sure you copied the entire key
- No extra spaces before/after

### "Want to use a different provider"
- Go to Settings
- Look for "Provider" or "LLM Provider" dropdown
- Select your preferred provider
- Add the corresponding API key

---

## Recommended Free Setup

For the easiest free setup:

1. **Get OpenRouter key** (free account)
2. **In Agent Zero Settings:**
   - Add OpenRouter API key
k   - **IMPORTANT**: Select a **free model** like: `meta-llama/llama-3.2-3b-instruct:free`
   - This prevents "402 Payment Required" errors
3. **Save and test**

### ⚠️ Important: Use Free Models

If you see this error:
```
APIError: This request requires more credits, or fewer max_tokens
```

**Solution**: Switch to a free model in Settings. See `FIX_CREDITS_ERROR.md` for details.

---

## Security Notes

⚠️ **Important:**
- Never share your API keys publicly
- Keys are stored securely in Agent Zero
- Monitor usage in your provider dashboard
- Rotate keys if compromised

---

## Need Help?

- **Agent Zero Docs**: Check the Settings page help text
- **OpenRouter Docs**: https://openrouter.ai/docs
- **GitHub Issues**: https://github.com/agent0ai/agent-zero/issues

---

## Quick Reference

| Provider | Free Tier | Get Key At |
|----------|-----------|------------|
| OpenRouter | ✅ Yes | https://openrouter.ai/keys |
| Google AI | ✅ Yes | https://aistudio.google.com/app/apikey |
| OpenAI | ❌ Paid | https://platform.openai.com/api-keys |
| Anthropic | ❌ Paid | https://console.anthropic.com/ |

---

**Once you add an API key, Agent Zero will work perfectly!** 🚀

