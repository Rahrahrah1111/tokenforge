# API Keys Setup Guide - Quick & Easy

## Why You Need to Do This Yourself

API providers require:
- Email verification
- Account creation with your own credentials
- Terms of service agreement
- Security best practices (you control your keys)

## Free API Keys Available

### 1. Google AI (Gemini) - FREE ✅
**Free Tier**: 60 requests/minute, 1,500 requests/day

**Steps:**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. In browser console (F12), run:
   ```javascript
   localStorage.setItem('GOOGLE_API_KEY', 'your-key-here');
   ```

**Alternative**: https://aistudio.google.com/app/apikey

---

### 2. Tavily Search - FREE ✅
**Free Tier**: 1,000 searches/month

**Steps:**
1. Go to: https://tavily.com
2. Click "Get Started" or "Sign Up"
3. Create account (email + password)
4. Verify email
5. Go to Dashboard → API Keys
6. Copy your API key
7. In browser console (F12), run:
   ```javascript
   localStorage.setItem('TAVILY_API_KEY', 'your-key-here');
   ```

---

### 3. Discord Bot Token - FREE ✅
**Free**: Unlimited (for personal bots)

**Steps:**
1. Go to: https://discord.com/developers/applications
2. Click "New Application"
3. Name it (e.g., "A.V.A. Bot")
4. Go to "Bot" section
5. Click "Add Bot" → "Yes, do it!"
6. Under "Token", click "Reset Token" or "Copy"
7. Copy the token
8. In browser console (F12), run:
   ```javascript
   localStorage.setItem('DISCORD_TOKEN', 'your-token-here');
   ```

**Note**: You'll also need to invite the bot to your server with proper permissions.

---

## Quick Setup Script

After obtaining your keys, you can run this in the browser console (F12):

```javascript
// Set your API keys
localStorage.setItem('GOOGLE_API_KEY', 'paste-google-key-here');
localStorage.setItem('TAVILY_API_KEY', 'paste-tavily-key-here');
localStorage.setItem('DISCORD_TOKEN', 'paste-discord-token-here');

// Verify they're set
console.log('Google Key:', localStorage.getItem('GOOGLE_API_KEY') ? '✅ Set' : '❌ Missing');
console.log('Tavily Key:', localStorage.getItem('TAVILY_API_KEY') ? '✅ Set' : '❌ Missing');
console.log('Discord Token:', localStorage.getItem('DISCORD_TOKEN') ? '✅ Set' : '❌ Missing');

// Reload page to activate
location.reload();
```

## Verification

After setting keys, refresh the A.V.A. page and check the console:
- You should see: "KeyMaster initialized: X Google keys, Y Tavily keys, Z Discord tokens"
- If you see "0 keys", check that you copied the keys correctly

## Troubleshooting

### Key Not Working?
1. **Check for extra spaces**: Copy keys carefully
2. **Verify key format**: 
   - Google: Usually starts with `AIza...`
   - Tavily: Usually starts with `tvly-...`
   - Discord: Usually a long alphanumeric string
3. **Check browser console** for specific error messages
4. **Try refreshing** the page after setting keys

### Rate Limits?
- **Google**: 60 requests/minute (free tier)
- **Tavily**: 1,000 searches/month (free tier)
- **Discord**: No limits for personal bots

### Multiple Keys?
You can set multiple keys for automatic rotation:
```javascript
localStorage.setItem('GOOGLE_API_KEY_1', 'key1');
localStorage.setItem('GOOGLE_API_KEY_2', 'key2');
localStorage.setItem('TAVILY_API_KEY_1', 'key1');
localStorage.setItem('TAVILY_API_KEY_2', 'key2');
```

## Security Best Practices

1. **Never share your API keys** publicly
2. **Don't commit keys** to git repositories
3. **Rotate keys** if you suspect they're compromised
4. **Use environment variables** in production (not localStorage)
5. **Monitor usage** in provider dashboards

## Alternative: Environment Variables (For Backend)

If you're running a backend server, use environment variables instead:

```bash
# .env file
GOOGLE_API_KEY=your-key
TAVILY_API_KEY=your-key
DISCORD_TOKEN=your-token
```

## What Each Key Enables

- **Google AI Key**: 
  - ✅ Advanced AI responses
  - ✅ Complex analysis
  - ✅ Context-aware generation

- **Tavily Key**:
  - ✅ Real-time web search
  - ✅ Answer generation
  - ✅ Research capabilities

- **Discord Token**:
  - ✅ Discord bot integration
  - ✅ Channel communication
  - ✅ Message sending

## Time Required

- **Google AI**: ~2 minutes
- **Tavily**: ~3 minutes (email verification)
- **Discord**: ~5 minutes (bot setup)

**Total**: ~10 minutes for all three

## Need Help?

If you encounter issues:
1. Check the browser console (F12) for errors
2. Verify keys are correctly formatted
3. Ensure you're signed in to the provider
4. Check if you've verified your email (Tavily)
5. Make sure the bot has proper permissions (Discord)

## Next Steps

After setting up keys:
1. Refresh the A.V.A. page
2. Try a research query: "Search for recent AI developments"
3. Try an analysis query: "Analyze the implications of quantum computing"
4. Check the console for "KeyMaster initialized" message

---

**Note**: All three services offer free tiers that are perfect for personal use and testing!

