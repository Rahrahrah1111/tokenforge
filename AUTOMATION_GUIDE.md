# API Keys Automation Guide

## 🚀 Quick Start

### Option 1: Automated Browser Script (Recommended)

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run automation:**
   ```bash
   npm run setup
   # or
   node automate_api_setup.js
   ```

3. **Follow the prompts:**
   - Enter your email
   - Enter password (optional, for auto-login)
   - The browser will open and guide you through each service
   - Keys will be automatically detected and saved

4. **Copy keys to browser:**
   - Open `api_keys_localStorage.js` (auto-generated)
   - Copy the contents
   - Open A.V.A. page (index.html)
   - Open browser console (F12)
   - Paste and press Enter

### Option 2: Browser Auto-Detector (Easiest)

1. **Open A.V.A. page** (index.html)

2. **Open browser console** (F12)

3. **Paste the auto-detector script:**
   ```javascript
   // Copy entire contents of auto_key_detector.js
   ```

4. **Sign up for services:**
   - Go to each service website
   - Sign up and get your API key
   - **Just copy the key** - it will be auto-detected and saved!

5. **Done!** Keys are automatically saved to localStorage

## 📋 Step-by-Step Process

### 1. Google AI (Gemini)

**Automated:**
- Script opens https://makersuite.google.com/app/apikey
- Detects if you're logged in
- Clicks "Create API Key"
- Auto-detects and saves the key

**Manual (if needed):**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)
5. Paste anywhere - auto-detector will catch it!

### 2. Tavily Search

**Automated:**
- Script opens https://tavily.com
- Clicks "Sign Up"
- Fills email/password (if provided)
- Navigates to API keys page
- Auto-detects and saves the key

**Manual (if needed):**
1. Go to: https://tavily.com
2. Click "Sign Up"
3. Verify email
4. Go to Dashboard → API Keys
5. Copy the key (starts with `tvly-...`)
6. Paste anywhere - auto-detector will catch it!

### 3. Discord Bot

**Automated:**
- Script opens https://discord.com/developers/applications
- Creates new application
- Navigates to Bot section
- Clicks "Add Bot" or "Reset Token"
- Auto-detects and saves the token

**Manual (if needed):**
1. Go to: https://discord.com/developers/applications
2. Click "New Application"
3. Name it "A.V.A. Bot"
4. Go to "Bot" section
5. Click "Add Bot" → "Yes, do it!"
6. Click "Reset Token" or "Copy"
7. Copy the token (long alphanumeric string)
8. Paste anywhere - auto-detector will catch it!

## 🎯 Auto-Detector Features

The browser auto-detector:

- ✅ **Monitors clipboard** - Detects keys when you copy them
- ✅ **Scans page content** - Finds keys on the page
- ✅ **Monitors input fields** - Detects keys as you type
- ✅ **Auto-saves** - Saves to localStorage immediately
- ✅ **Shows notifications** - Visual confirmation when keys are saved
- ✅ **Updates status** - Updates setup page status indicators

## 🔧 Manual Functions

If auto-detector is running, you can also use:

```javascript
// Detect keys in text
detectAPIKeys("Your text with AIza... key here");

// Save key manually
saveAPIKey("google", "AIza...");
saveAPIKey("tavily", "tvly-...");
saveAPIKey("discord", "M...");
```

## 📁 Generated Files

After running automation, you'll get:

1. **api_keys_localStorage.js** - Copy/paste into browser console
2. **.env** - For Node.js/backend use
3. **api_keys.json** - JSON format for other uses

## 🐛 Troubleshooting

### Automation script fails?
- Make sure Node.js is installed: `node --version`
- Install dependencies: `npm install`
- Check browser opens correctly
- Some steps may need manual completion (CAPTCHA, email verification)

### Auto-detector not working?
- Make sure script is pasted in console
- Check browser console for errors
- Try refreshing the page
- Manually use `saveAPIKey()` function

### Keys not saving?
- Check browser allows localStorage
- Try incognito/private mode (may block localStorage)
- Check browser console for errors
- Manually save: `localStorage.setItem('GOOGLE_API_KEY', 'your-key')`

### Can't find keys on page?
- Some services hide keys initially
- Look for "Show" or "Reveal" buttons
- Check if you need to click "Create" first
- Use manual detection: `detectAPIKeys(pageText)`

## 🎨 Customization

### Change key patterns:
Edit `auto_key_detector.js`:
```javascript
const keyPatterns = {
    google: /AIza[0-9A-Za-z_-]{35}/,
    tavily: /tvly-[0-9A-Za-z_-]{20,}/,
    discord: /[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}/,
    // Add your own patterns here
    custom: /your-pattern-here/
};
```

### Change storage keys:
Edit `auto_key_detector.js`:
```javascript
const keyNames = {
    google: 'GOOGLE_API_KEY',
    tavily: 'TAVILY_API_KEY',
    discord: 'DISCORD_TOKEN',
    // Add your own keys here
    custom: 'CUSTOM_API_KEY'
};
```

## 🔒 Security Notes

- Keys are stored in browser localStorage (client-side only)
- Never commit keys to git repositories
- Use `.env` file for backend (add to `.gitignore`)
- Rotate keys if compromised
- Monitor API usage in provider dashboards

## 📊 Status Check

Check which keys are set:
```javascript
// In browser console
console.log('Google:', localStorage.getItem('GOOGLE_API_KEY') ? '✅' : '❌');
console.log('Tavily:', localStorage.getItem('TAVILY_API_KEY') ? '✅' : '❌');
console.log('Discord:', localStorage.getItem('DISCORD_TOKEN') ? '✅' : '❌');
```

## 🚀 Next Steps

After keys are saved:

1. **Refresh A.V.A. page** (index.html)
2. **Check console** for "KeyMaster initialized" message
3. **Test with queries:**
   - "Search for recent AI developments" (uses Tavily)
   - "Analyze quantum computing" (uses Google AI)
4. **Enjoy enhanced A.V.A. capabilities!**

## 💡 Tips

- **Start with one service** - Get comfortable with the process
- **Use auto-detector** - It makes the process much easier
- **Keep browser console open** - See what's happening
- **Check notifications** - Visual feedback when keys are saved
- **Save backup** - Copy keys to a secure password manager

---

**Need help?** Check the browser console for detailed logs and error messages.

