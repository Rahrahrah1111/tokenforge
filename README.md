## OKComputer A.V.A. Chat Integration

Modern AI automation stack combining:

- **Agent Zero Orchestration** – multi-agent control and automation
- **TokenForge Chat** – multi-LLM chat UI with automatic token compression
- **Wyze Analyzer** – audio/video event detection and transcription pipeline

This repo is structured so you can run it locally or package it as a productized AI toolkit.

### Key Components

- **`tokenforge/`**: Embedded TokenForge library (compression, privacy, adapters)
- **`tokenforge_chat_app.py`**: Gradio interface for chatting with multiple LLMs (OpenAI, Anthropic, Groq, Ollama, generic APIs) with TokenForge compression enabled by default
- **`wyze_analyzer/`**: Tools for analyzing Wyze camera audio/video, with dashboards and batch processing
- **Agent Zero scripts**: Setup and automation scripts (`AGENT_ZERO_SETUP.md`, `start_agent_zero.sh`, etc.)

### Quick Start – TokenForge Chat

```bash
cd "OKComputer_A.V.A. Chat Integration"

# (Recommended) Use the existing venv for tokenforge_chat
source tokenforge_chat_venv/bin/activate  # or `source tokenforge/venv/bin/activate`

python tokenforge_chat_app.py
```

Open your browser at `http://localhost:7860` to use the chat interface.

See `TOKENFORGE_CHAT_SETUP.md` and `TOKENFORGE_CHAT_README.md` for full instructions and marketing-ready copy.

### Packaging / Selling

- Keep `tokenforge/` and `tokenforge_chat_app.py` together as the **TokenForge Chat product module**
- The `.gitignore` is set up to exclude heavy data, venvs, and build artifacts so the repo stays clean
- You can publish this repo directly to GitHub as a **demo + product**:
  - Token-efficient multi-LLM chat UI
  - Extensible agents and automation scripts
  - Optional Wyze Analyzer add-on


