# 🔥 TokenForge Chat Application Setup

Multi-LLM chat interface with automatic token compression - test TokenForge with different AI models!

## 🚀 Quick Start

### 1. Install TokenForge

First, install TokenForge from the local directory:

```bash
cd tokenforge
pip install -e .
cd ..
```

### 2. Install Chat App Dependencies

```bash
pip install -r tokenforge_chat_requirements.txt
```

Or install individually:

```bash
pip install gradio>=4.0.0 openai>=1.0.0 anthropic>=0.18.0
```

### 3. Set API Keys (Optional)

You can set API keys as environment variables or enter them in the UI:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic (Claude)
export ANTHROPIC_API_KEY="sk-ant-..."

# Groq
export GROQ_API_KEY="gsk_..."
```

### 4. Run the Application

```bash
python tokenforge_chat_app.py
```

The app will launch at `http://localhost:7860`

## 📋 Available Chat Interfaces

### 🤖 OpenAI (GPT-4)
- Models: gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo
- Requires: OpenAI API key
- Set `OPENAI_API_KEY` environment variable or enter in UI

### 🧠 Anthropic (Claude)
- Models: Claude Sonnet 4, Claude 3.5 Sonnet, Claude 3 Opus, etc.
- Requires: Anthropic API key
- Set `ANTHROPIC_API_KEY` environment variable or enter in UI

### ⚡ Groq (Fast Inference)
- Models: Llama 3.1 70B, Llama 3.1 8B, Mixtral, Gemma
- Requires: Groq API key (free tier available)
- Set `GROQ_API_KEY` environment variable or enter in UI

### 🦙 Ollama (Local)
- Models: Any Ollama model (llama3.2, mistral, etc.)
- Requires: Ollama running locally
- Default URL: `http://localhost:11434/v1`
- Install Ollama: https://ollama.ai

### 🔌 Generic API
- Works with: LM Studio, vLLM, Together.ai, or any OpenAI-compatible API
- Configure base URL and model name
- Optional API key if required

## 💡 How It Works

1. **You type a message** - Just like ChatGPT!
2. **TokenForge automatically compresses it** - Reduces tokens by 40-70%
3. **LLM receives compressed message** - LLM can decompress using the public dictionary
4. **You get the response** - Same quality, lower cost!
5. **See your savings** - Real-time statistics show tokens saved

## 📊 Features

- ✅ **Automatic Compression** - No code changes needed
- ✅ **Privacy Shield** - PII detection and redaction
- ✅ **Real-time Stats** - See tokens saved and cost reduction
- ✅ **Multi-LLM Support** - Test with different models
- ✅ **Chat History** - Conversation context maintained
- ✅ **Cost Tracking** - Estimated savings displayed

## 🎯 Example Usage

1. Open the app in your browser
2. Select a chat tab (e.g., OpenAI)
3. Enter your API key (or use environment variable)
4. Type a message like: "Explain quantum computing in detail"
5. Watch TokenForge compress it automatically
6. See the response and compression stats!

## 🔧 Troubleshooting

### TokenForge Not Available
```bash
cd tokenforge
pip install -e .
```

### Missing Dependencies
```bash
pip install gradio openai anthropic requests
```

### API Key Errors
- Make sure your API key is valid
- Check environment variables are set correctly
- Or enter the key directly in the UI

### Ollama Connection Issues
- Make sure Ollama is running: `ollama serve`
- Check the base URL matches your Ollama setup
- Verify the model name is correct

## 📈 Compression Stats

Each chat interface shows:
- Total requests
- Input vs compressed characters
- Compression ratio
- Tokens sent/received
- **Tokens saved** (the key metric!)
- Estimated cost savings
- PII items redacted

## 🎉 Benefits

- **40-70% token reduction** on average
- **Automatic** - zero configuration needed
- **Universal** - works with any LLM
- **Privacy** - PII automatically redacted
- **Transparent** - see exactly what's saved

Enjoy chatting with reduced costs! 🚀


