# Local LLM Setup Guide for A.V.A.

A.V.A. can use local LLMs for intelligent, natural conversations. Here's how to set it up:

## Quick Start with Ollama

### 1. Install Ollama
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Or download from: https://ollama.com/download
```

### 2. Start Ollama
```bash
ollama serve
```

### 3. Download Recommended Models

**For 16GB RAM Systems (4-8GB models):**

**Best Quality/Size Balance - Llama 3.2 3B (~2GB):**
```bash
ollama pull llama3.2:3b
```
- Excellent quality for size
- Very fast responses
- Only ~2GB RAM usage
- Perfect for 16GB systems

**Higher Quality - Llama 3.1 8B (~4.5GB):**
```bash
ollama pull llama3.1:8b
```
- Better quality than 3B
- Still fits comfortably in 16GB
- Great balance

**Excellent Alternative - Mistral 7B (~4GB):**
```bash
ollama pull mistral:7b
```
- Very efficient
- Great quality
- Well optimized

**Microsoft's Efficient Model - Phi-3 Medium (~4GB):**
```bash
ollama pull phi3:medium
```
- Highly optimized
- Great for smaller systems

**Ultra-Fast Option - Llama 3.2 1B (~700MB):**
```bash
ollama pull llama3.2:1b
```
- Fastest option
- Still quite capable
- Minimal RAM usage

### 4. Verify Installation
```bash
ollama list
```

You should see your downloaded models listed.

## Model Recommendations

### For 16GB RAM Systems (RECOMMENDED):
- **llama3.2:3b** (~2GB) - ⭐ BEST CHOICE - Excellent quality, very fast, perfect for 16GB
- **llama3.1:8b** (~4.5GB) - Great quality, still fits comfortably
- **mistral:7b** (~4GB) - Very efficient, excellent quality
- **phi3:medium** (~4GB) - Highly optimized, great performance
- **qwen2:7b** (~4.5GB) - Very capable, efficient
- **llama3.2:1b** (~700MB) - Ultra-fast, minimal RAM, still capable

### For Systems with More RAM (32GB+):
- **llama3.3:70b** - Top choice, most intelligent
- **mixtral:8x7b** - Excellent alternative, very capable
- **llama3.1:70b** - Great quality, slightly older

## System Requirements

### For 16GB RAM Systems (Recommended):

**Llama 3.2 3B:**
- **RAM**: 4-6GB usage (perfect for 16GB systems)
- **VRAM**: 2GB+ for GPU acceleration (optional)
- **Storage**: ~2GB
- **Speed**: Very fast responses

**Llama 3.1 8B:**
- **RAM**: 6-8GB usage (comfortable on 16GB)
- **VRAM**: 4GB+ for GPU acceleration
- **Storage**: ~4.5GB
- **Speed**: Fast responses

**Mistral 7B:**
- **RAM**: 5-7GB usage
- **VRAM**: 4GB+ for GPU acceleration
- **Storage**: ~4GB
- **Speed**: Fast, well optimized

**Phi-3 Medium:**
- **RAM**: 4-6GB usage
- **VRAM**: 3GB+ for GPU acceleration
- **Storage**: ~4GB
- **Speed**: Very fast, highly optimized

**Llama 3.2 1B:**
- **RAM**: 1-2GB usage (ultra-lightweight)
- **VRAM**: 1GB+ for GPU acceleration
- **Storage**: ~700MB
- **Speed**: Extremely fast

### For Systems with More RAM (32GB+):

**Llama 3.3 70B:**
- **RAM**: 48GB+ recommended
- **VRAM**: 40GB+ for GPU acceleration
- **Storage**: ~40GB

**Mixtral 8x7B:**
- **RAM**: 48GB+ recommended
- **VRAM**: 48GB+ for GPU acceleration
- **Storage**: ~26GB

## How A.V.A. Uses Local LLMs

1. **Automatic Detection**: A.V.A. automatically detects if Ollama is running
2. **Model Selection**: Automatically selects the best available model from:
   - llama3.3:70b
   - llama3.3
   - llama3.1:70b
   - mixtral:8x7b
   - mistral
   - llama2

3. **Fallback**: If no LLM is available, A.V.A. uses intelligent dynamic generation

## Testing Your Setup

1. Start Ollama: `ollama serve`
2. Pull a model: `ollama pull llama3.3:70b`
3. Refresh the A.V.A. page
4. Check the status message - it should show "✓ Local LLM Connected"

## Troubleshooting

### Ollama not detected?
- Make sure Ollama is running: `ollama serve`
- Check if it's on port 11434: `curl http://localhost:11434/api/tags`
- Try restarting Ollama

### Model not found?
- Make sure you've pulled the model: `ollama pull llama3.3:70b`
- Check available models: `ollama list`
- A.V.A. will use the best available model automatically

### Slow responses?
- If using a large model, switch to `llama3.2:3b` for much faster responses
- Enable GPU acceleration if available: `OLLAMA_GPU_ENABLED=1 ollama serve`
- Close other memory-intensive applications

### Out of memory?
- Use `llama3.2:3b` or `llama3.2:1b` for minimal RAM usage
- Close other applications to free up RAM
- Consider using CPU-only mode (slower but uses less VRAM)
- Check RAM usage: `free -h` (Linux) or Activity Monitor (Mac)

### Best Model for 16GB RAM?
**Recommended: `llama3.2:3b`**
- Only uses ~2GB RAM
- Excellent quality for its size
- Very fast responses
- Perfect balance for 16GB systems

## Advanced: Using Other Local Servers

A.V.A. can also connect to:
- **DeepPavlov**: Configure at `http://localhost:5000`
- **Custom API**: Modify `servers` object in `main.js`

## Benefits of Local LLMs

✅ **Privacy**: All processing happens locally
✅ **No API costs**: Free to use
✅ **Unlimited usage**: No rate limits
✅ **Customizable**: Full control over models and parameters
✅ **Offline capable**: Works without internet

Enjoy your enhanced A.V.A. experience!

