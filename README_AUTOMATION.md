# 🤖 Automated API Key Setup

## Overview

This automation system makes getting API keys for A.V.A. as easy as possible. After you sign up for one service, the system helps you get the rest automatically.

## 🎯 Two Ways to Use

### Method 1: Browser Auto-Detector (Easiest - Recommended)

1. **Open `quick_setup.html`** in your browser
2. **Click "Get Free Key →"** for each service
3. **Sign up and get your API key**
4. **Just copy the key** - it's automatically detected and saved! ✨
5. **Done!** No manual pasting needed.

**That's it!** The auto-detector does everything.

---

### Method 2: Full Browser Automation

For complete hands-off automation:

```bash
# Install once
npm install

# Run automation
npm run setup
# or
./run_automation.sh
```

The script will:
- Open browser windows
- Guide you through signups
- Auto-detect API keys
- Save them automatically
- Generate ready-to-use files

---

## 🔍 How Auto-Detection Works

The auto-detector (included in `quick_setup.html`) monitors:

1. **📋 Clipboard** - When you copy a key
2. **📄 Page Content** - Keys visible on the page  
3. **⌨️ Input Fields** - Keys you type

**Just copy/paste anywhere** and it's automatically saved!

---

## 📋 What Gets Automated

### ✅ Google AI (Gemini)
- Opens signup page
- Detects login status
- Clicks "Create API Key"
- Auto-detects key format: `AIza...`

### ✅ Tavily Search
- Opens signup page
- Fills email/password (if provided)
- Navigates to API keys
- Auto-detects key format: `tvly-...`

### ✅ Discord Bot
- Opens developer portal
- Creates new application
- Navigates to Bot section
- Auto-detects token format: `M...`

---

## 🚀 Quick Start

### Option A: Just Use the Browser (30 seconds)

1. Open `quick_setup.html`
2. Click "Get Free Key →" links
3. Sign up and copy keys
4. Done! Keys are auto-saved

### Option B: Full Automation (2 minutes)

```bash
npm install
npm run setup
```

Follow the prompts, and keys are automatically saved.

---

## 📁 Generated Files

After automation, you'll get:

- **api_keys_localStorage.js** - Copy/paste into browser console
- **.env** - For Node.js/backend use  
- **api_keys.json** - JSON format

---

## 🎨 Features

- ✅ **Auto-detection** - Finds keys automatically
- ✅ **Auto-save** - Saves to localStorage immediately
- ✅ **Visual feedback** - Shows notifications when keys are saved
- ✅ **Status updates** - Updates setup page in real-time
- ✅ **Multiple formats** - Generates files for different uses
- ✅ **Error handling** - Graceful fallbacks if automation fails

---

## 🔧 Manual Override

If auto-detection doesn't work:

```javascript
// In browser console
saveAPIKey("google", "AIza...");
saveAPIKey("tavily", "tvly-...");
saveAPIKey("discord", "M...");
```

Or use the input fields on `quick_setup.html`.

---

## 🐛 Troubleshooting

**Auto-detector not working?**
- Make sure `auto_key_detector.js` is loaded
- Check browser console for errors
- Try refreshing the page

**Automation script fails?**
- Make sure Node.js is installed: `node --version`
- Install dependencies: `npm install`
- Some steps may need manual completion (CAPTCHA, email verification)

**Keys not saving?**
- Check browser allows localStorage
- Try incognito/private mode (may block localStorage)
- Manually save: `localStorage.setItem('GOOGLE_API_KEY', 'your-key')`

---

## 📊 Check Status

```javascript
// In browser console
console.log('Google:', localStorage.getItem('GOOGLE_API_KEY') ? '✅' : '❌');
console.log('Tavily:', localStorage.getItem('TAVILY_API_KEY') ? '✅' : '❌');
console.log('Discord:', localStorage.getItem('DISCORD_TOKEN') ? '✅' : '❌');
```

---

## 🎯 Next Steps

After keys are saved:

1. **Refresh A.V.A. page** (index.html)
2. **Check console** for "KeyMaster initialized" message
3. **Test with queries:**
   - "Search for recent AI developments" (uses Tavily)
   - "Analyze quantum computing" (uses Google AI)
4. **Enjoy enhanced capabilities!**

---

## 💡 Pro Tips

- **Start with one service** - Get comfortable with the process
- **Use auto-detector** - It makes everything easier
- **Keep console open** - See what's happening
- **Check notifications** - Visual feedback when keys are saved
- **Save backup** - Copy keys to a secure password manager

---

## 📚 More Info

- **AUTOMATION_GUIDE.md** - Detailed instructions
- **API_KEYS_SETUP_GUIDE.md** - Manual setup guide
- **QUICK_START.md** - Quick reference

---

**That's it!** The automation handles everything. Just sign up and copy keys - the rest is automatic! 🎉

