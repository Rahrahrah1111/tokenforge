# 🔥 TokenForge Chat - Multi-LLM Testing Interface

Test TokenForge compression with multiple AI models! This application provides chat interfaces for different LLMs, all with automatic token compression enabled.

## 🎯 What This Does

- **Automatic Compression**: Every message you send is automatically compressed by TokenForge before being sent to the LLM
- **Cost Reduction**: Save 40-70% on token costs without any code changes
- **Multi-LLM Support**: Test with OpenAI, Anthropic, Groq, Ollama, and generic APIs
- **Real-time Stats**: See exactly how many tokens you're saving
- **Privacy Protection**: PII is automatically detected and redacted

## 🚀 Quick Start

### Option 1: Use the startup script
```bash
./start_tokenforge_chat.sh
```

### Option 2: Manual setup
```bash
# 1. Install TokenForge
cd tokenforge
pip install -e .
cd ..

# 2. Install dependencies
pip install gradio openai anthropic

# 3. Run the app
python tokenforge_chat_app.py
```

The app will open at `http://localhost:7860`

## 📋 Supported LLMs

### 🤖 OpenAI (GPT-4, GPT-3.5)
- Set `OPENAI_API_KEY` environment variable or enter in UI
- Models: gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo

### 🧠 Anthropic (Claude)
- Set `ANTHROPIC_API_KEY` environment variable or enter in UI
- Models: Claude Sonnet 4, Claude 3.5 Sonnet, Claude 3 Opus

### ⚡ Groq (Fast Inference)
- Set `GROQ_API_KEY` environment variable or enter in UI
- Models: Llama 3.1 70B, Llama 3.1 8B, Mixtral, Gemma
- Free tier available!

### 🦙 Ollama (Local)
- Requires Ollama running locally
- Default: `http://localhost:11434/v1`
- Any Ollama model (llama3.2, mistral, etc.)

### 🔌 Generic API
- Works with any OpenAI-compatible API
- LM Studio, vLLM, Together.ai, etc.
- Configure base URL and model name

## 💡 How It Works

1. **You type a message** - Just like ChatGPT!
2. **TokenForge compresses it** - Reduces tokens by 40-70%
3. **LLM receives compressed message** - LLM decompresses using public dictionary
4. **You get the response** - Same quality, lower cost!
5. **See your savings** - Real-time statistics

## 📊 Example

**Original Message:**
```
Please help me write a Python function that validates email addresses and handles authentication for my web application.
```

**After TokenForge Compression:**
```
PHM W> fn VL> EMAIL & HD> AUTH 4 WEB APP
```

**Token Reduction**: ~67% fewer tokens!

## 🎨 Features

- ✅ **Chat Interface** - Clean, ChatGPT-like UI
- ✅ **Multiple Tabs** - One tab per LLM provider
- ✅ **Real-time Stats** - See compression ratio, tokens saved, cost savings
- ✅ **Chat History** - Conversation context maintained
- ✅ **Privacy Shield** - Automatic PII redaction
- ✅ **No Code Changes** - Works automatically

## 📈 Statistics Displayed

Each chat shows:
- Total requests
- Input vs compressed characters
- Compression ratio (%)
- Tokens sent/received
- **Tokens saved** (key metric!)
- Estimated cost savings ($)
- PII items redacted

## 🔧 Configuration

### Environment Variables
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GROQ_API_KEY="gsk_..."
```

### Or Enter in UI
You can also enter API keys directly in each chat tab's configuration panel.

## 🐛 Troubleshooting

**TokenForge not found?**
```bash
cd tokenforge && pip install -e .
```

**Missing dependencies?**
```bash
pip install gradio openai anthropic requests
```

**API errors?**
- Check your API key is valid
- Verify environment variables are set
- Or enter key directly in UI

**Ollama not connecting?**
- Make sure Ollama is running: `ollama serve`
- Check the base URL matches your setup
- Verify model name is correct

## 🎉 Benefits

- **40-70% token reduction** on average
- **Automatic** - zero configuration
- **Universal** - works with any LLM
- **Privacy** - PII automatically protected
- **Transparent** - see exactly what's saved

## 📚 Learn More

- [TokenForge GitHub](https://github.com/tokenforge/tokenforge)
- [TokenForge PyPI](https://pypi.org/project/tokenforge/)
- [Setup Guide](TOKENFORGE_CHAT_SETUP.md)

---

**Enjoy chatting with reduced costs!** 🚀💰


