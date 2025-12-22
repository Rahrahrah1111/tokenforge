# 🔧 Fix: OpenRouter Credits Error

## The Error

```
APIError: This request requires more credits, or fewer max_tokens. 
You requested up to 64000 tokens, but can only afford 4717.
```

## ✅ Solution: Use a Free Model

The issue is that Agent Zero is trying to use a paid model that requires credits. Switch to a **free model** instead.

---

## Quick Fix (2 minutes)

### Option 1: Switch to Free Model in Agent Zero Settings

1. **Open Agent Zero**: http://localhost:50001
2. **Click Settings** (⚙️ icon)
3. **Find "Model" or "LLM Model"** dropdown
4. **Select a FREE model**, such as:
   - `meta-llama/llama-3.2-3b-instruct:free`
   - `google/gemini-flash-1.5-8b:free`
   - `mistralai/mistral-7b-instruct:free`
   - `qwen/qwen-2.5-7b-instruct:free`
5. **Save settings**
6. **Try again** - should work now! ✅

---

### Option 2: Reduce Max Tokens

If you want to keep your current model:

1. **Open Settings** in Agent Zero
2. **Find "Max Tokens"** or "Max Response Length"
3. **Reduce it to 4000** or less
4. **Save settings**

---

### Option 3: Use Google AI (Gemini) - Completely Free

Switch to Google AI which has a generous free tier:

1. **Get Google AI Key** (free):
   - Go to: https://aistudio.google.com/app/apikey
   - Create API key (free, no credit card needed)

2. **In Agent Zero Settings**:
   - Change **Provider** to "Google AI" or "Gemini"
   - Add your Google API key
   - Select model: `gemini-1.5-flash` or `gemini-1.5-pro`
   - Save

3. **Test** - Should work perfectly! ✅

---

## Recommended Free Models on OpenRouter

These models are **completely free** (no credits needed):

| Model | Best For |
|-------|----------|
| `meta-llama/llama-3.2-3b-instruct:free` | General chat, fast responses |
| `google/gemini-flash-1.5-8b:free` | Google's free model |
| `mistralai/mistral-7b-instruct:free` | Good quality, fast |
| `qwen/qwen-2.5-7b-instruct:free` | Multilingual support |
| `microsoft/phi-3-mini-128k-instruct:free` | Small, efficient |

**Note**: Free models have rate limits but are perfect for getting started!

---

## How to Find Free Models

1. Go to: https://openrouter.ai/models
2. Filter by: **"Free"** or **"No Credit Required"**
3. Copy the model name
4. Use it in Agent Zero Settings

---

## Alternative: Add Credits to OpenRouter

If you want to use paid models:

1. Go to: https://openrouter.ai/settings/credits
2. Add credits (minimum $5)
3. Your current model will work

**But free models work great for most use cases!**

---

## Quick Reference

**Problem**: Request needs 64,000 tokens, but only have credits for 4,717

**Solutions**:
1. ✅ Switch to free model (easiest)
2. ✅ Reduce max_tokens to 4000
3. ✅ Use Google AI instead (completely free)
4. ✅ Add credits to OpenRouter account

---

## Recommended Setup for Free Usage

1. **Keep OpenRouter API key** (you already have it)
2. **In Agent Zero Settings**:
   - Model: `meta-llama/llama-3.2-3b-instruct:free`
   - Max Tokens: 4000 (or leave default)
3. **Save and test**

This gives you:
- ✅ No credit card needed
- ✅ Free to use
- ✅ Good quality responses
- ✅ Fast responses

---

**Once you switch to a free model, everything will work perfectly!** 🚀






