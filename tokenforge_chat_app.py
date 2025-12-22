#!/usr/bin/env python3
"""
TokenForge Chat Application
Multi-LLM chat interface with automatic token compression

Test TokenForge with different AI models - compression happens automatically!
"""

import os
import sys
import gradio as gr
from typing import List, Tuple, Optional, Dict, Any
import json

# Add tokenforge to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tokenforge"))

try:
    from tokenforge import TokenForge, ForgeConfig, CompressionLevel
    from tokenforge.adapters import (
        OpenAIAdapter, 
        AnthropicAdapter, 
        GenericAdapter,
        Message
    )
    TOKENFORGE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: TokenForge not available: {e}")
    TOKENFORGE_AVAILABLE = False

# Global state for each chat session
chat_sessions: Dict[str, Any] = {}


def create_forge_instance(adapter_type: str, api_key: Optional[str] = None, 
                          model: Optional[str] = None, base_url: Optional[str] = None) -> Optional[TokenForge]:
    """Create a TokenForge instance with the specified adapter."""
    if not TOKENFORGE_AVAILABLE:
        return None
    
    try:
        # Configure compression
        config = ForgeConfig(
            compression_level=CompressionLevel.STANDARD,
            auto_compress=True,
            enable_privacy=True,
            include_decoder_prompt=True
        )
        
        # Create adapter based on type
        if adapter_type == "openai":
            adapter = OpenAIAdapter(
                api_key=api_key or os.environ.get("OPENAI_API_KEY"),
                model=model or "gpt-4o"
            )
        elif adapter_type == "anthropic":
            adapter = AnthropicAdapter(
                api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"),
                model=model or "claude-sonnet-4-20250514"
            )
        elif adapter_type == "groq":
            adapter = GenericAdapter(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key or os.environ.get("GROQ_API_KEY"),
                model=model or "llama-3.1-70b-versatile"
            )
        elif adapter_type == "ollama":
            adapter = GenericAdapter(
                base_url=base_url or "http://localhost:11434/v1",
                api_key="not-needed",
                model=model or "llama3.2"
            )
        elif adapter_type == "generic":
            adapter = GenericAdapter(
                base_url=base_url or "http://localhost:1234/v1",
                api_key=api_key or "not-needed",
                model=model or "default"
            )
        else:
            return None
        
        return TokenForge(adapter=adapter, config=config)
    except Exception as e:
        print(f"Error creating forge instance: {e}")
        return None


def format_stats(stats: Dict[str, Any]) -> str:
    """Format statistics for display."""
    return f"""
### 📊 TokenForge Statistics

| Metric | Value |
|--------|-------|
| **Total Requests** | {stats.get('total_requests', 0)} |
| **Input Characters** | {stats.get('total_input_chars', 0):,} |
| **Compressed Characters** | {stats.get('total_compressed_chars', 0):,} |
| **Compression Ratio** | {stats.get('compression_ratio', '0%')} |
| **Tokens Sent** | {stats.get('total_tokens_sent', 0):,} |
| **Tokens Received** | {stats.get('total_tokens_received', 0):,} |
| **Tokens Saved** | {stats.get('total_tokens_saved', 0):,} |
| **💰 Estimated Savings** | {stats.get('estimated_cost_savings', '$0.0000')} |
| **🔒 PII Redacted** | {stats.get('total_pii_redacted', 0)} |

💡 **TokenForge is automatically compressing your messages to reduce costs!**
"""


def chat_openai(message: str, history: List[List[str]], api_key: str, model: str) -> Tuple[List[List[str]], str]:
    """Chat with OpenAI using TokenForge."""
    if not message.strip():
        return history, ""
    
    session_id = "openai"
    
    # Initialize or get existing forge instance
    if session_id not in chat_sessions or chat_sessions[session_id] is None:
        chat_sessions[session_id] = create_forge_instance("openai", api_key, model)
    
    forge = chat_sessions[session_id]
    
    if forge is None:
        error_msg = "❌ Failed to initialize TokenForge with OpenAI. Check your API key."
        history.append([message, error_msg])
        return history, error_msg
    
    try:
        # Send message through TokenForge (automatic compression!)
        response = forge.chat(message)
        
        # Get stats
        stats = forge.stats.to_dict()
        stats_text = format_stats(stats)
        
        # Update history
        history.append([message, response])
        
        return history, stats_text
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append([message, error_msg])
        return history, ""


def chat_anthropic(message: str, history: List[List[str]], api_key: str, model: str) -> Tuple[List[List[str]], str]:
    """Chat with Anthropic Claude using TokenForge."""
    if not message.strip():
        return history, ""
    
    session_id = "anthropic"
    
    if session_id not in chat_sessions or chat_sessions[session_id] is None:
        chat_sessions[session_id] = create_forge_instance("anthropic", api_key, model)
    
    forge = chat_sessions[session_id]
    
    if forge is None:
        error_msg = "❌ Failed to initialize TokenForge with Anthropic. Check your API key."
        history.append([message, error_msg])
        return history, error_msg
    
    try:
        response = forge.chat(message)
        stats = forge.stats.to_dict()
        stats_text = format_stats(stats)
        
        history.append([message, response])
        return history, stats_text
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append([message, error_msg])
        return history, ""


def chat_groq(message: str, history: List[List[str]], api_key: str, model: str) -> Tuple[List[List[str]], str]:
    """Chat with Groq using TokenForge."""
    if not message.strip():
        return history, ""
    
    session_id = "groq"
    
    if session_id not in chat_sessions or chat_sessions[session_id] is None:
        chat_sessions[session_id] = create_forge_instance("groq", api_key, model)
    
    forge = chat_sessions[session_id]
    
    if forge is None:
        error_msg = "❌ Failed to initialize TokenForge with Groq. Check your API key."
        history.append([message, error_msg])
        return history, error_msg
    
    try:
        response = forge.chat(message)
        stats = forge.stats.to_dict()
        stats_text = format_stats(stats)
        
        history.append([message, response])
        return history, stats_text
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append([message, error_msg])
        return history, ""


def chat_ollama(message: str, history: List[List[str]], base_url: str, model: str) -> Tuple[List[List[str]], str]:
    """Chat with Ollama using TokenForge."""
    if not message.strip():
        return history, ""
    
    session_id = "ollama"
    
    if session_id not in chat_sessions or chat_sessions[session_id] is None:
        chat_sessions[session_id] = create_forge_instance("ollama", None, model, base_url)
    
    forge = chat_sessions[session_id]
    
    if forge is None:
        error_msg = "❌ Failed to initialize TokenForge with Ollama. Make sure Ollama is running."
        history.append([message, error_msg])
        return history, error_msg
    
    try:
        response = forge.chat(message)
        stats = forge.stats.to_dict()
        stats_text = format_stats(stats)
        
        history.append([message, response])
        return history, stats_text
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append([message, error_msg])
        return history, ""


def chat_generic(message: str, history: List[List[str]], base_url: str, api_key: str, model: str) -> Tuple[List[List[str]], str]:
    """Chat with generic OpenAI-compatible API using TokenForge."""
    if not message.strip():
        return history, ""
    
    session_id = "generic"
    
    if session_id not in chat_sessions or chat_sessions[session_id] is None:
        chat_sessions[session_id] = create_forge_instance("generic", api_key, model, base_url)
    
    forge = chat_sessions[session_id]
    
    if forge is None:
        error_msg = "❌ Failed to initialize TokenForge. Check your API endpoint."
        history.append([message, error_msg])
        return history, error_msg
    
    try:
        response = forge.chat(message)
        stats = forge.stats.to_dict()
        stats_text = format_stats(stats)
        
        history.append([message, response])
        return history, stats_text
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append([message, error_msg])
        return history, ""


def clear_chat(chat_type: str):
    """Clear chat history and reset session."""
    if chat_type in chat_sessions and chat_sessions[chat_type]:
        chat_sessions[chat_type].new_session()
    return [], ""  # Return empty history and empty stats


# Create Gradio interface
with gr.Blocks(
    title="🔥 TokenForge Chat - Multi-LLM with Auto Compression",
    theme=gr.themes.Soft(primary_hue="orange"),
    css="""
    .gradio-container { max-width: 1400px !important; }
    .chat-container { height: 600px; }
    """
) as demo:
    
    gr.Markdown("""
    # 🔥 TokenForge Chat
    ### Chat with Multiple LLMs - Automatic Token Compression Reduces Costs by 40-70%
    
    **How it works**: TokenForge automatically compresses your messages before sending them to the LLM,
    then the LLM decompresses them. You save tokens and money, with zero effort!
    
    ---
    """)
    
    with gr.Tabs():
        # Tab 1: OpenAI
        with gr.TabItem("🤖 OpenAI (GPT-4)"):
            with gr.Row():
                with gr.Column(scale=2):
                    openai_chat = gr.Chatbot(
                        label="Chat with GPT-4 (TokenForge Enabled)",
                        height=500,
                        show_copy_button=True
                    )
                    openai_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Type your message here... TokenForge will automatically compress it!",
                        lines=3
                    )
                    with gr.Row():
                        openai_send = gr.Button("Send", variant="primary")
                        openai_clear = gr.Button("Clear Chat")
                
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Configuration")
                    openai_api_key = gr.Textbox(
                        label="OpenAI API Key",
                        type="password",
                        placeholder="sk-... (or set OPENAI_API_KEY env var)",
                        value=os.environ.get("OPENAI_API_KEY", "")
                    )
                    openai_model = gr.Dropdown(
                        choices=["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
                        value="gpt-4o",
                        label="Model"
                    )
                    openai_stats = gr.Markdown("### 📊 Statistics\n\n*Send a message to see compression stats*")
            
            openai_send.click(
                chat_openai,
                inputs=[openai_input, openai_chat, openai_api_key, openai_model],
                outputs=[openai_chat, openai_stats]
            )
            openai_input.submit(
                chat_openai,
                inputs=[openai_input, openai_chat, openai_api_key, openai_model],
                outputs=[openai_chat, openai_stats]
            )
            openai_clear.click(
                lambda: clear_chat("openai"),
                outputs=[openai_chat, openai_stats]
            )
        
        # Tab 2: Anthropic
        with gr.TabItem("🧠 Anthropic (Claude)"):
            with gr.Row():
                with gr.Column(scale=2):
                    anthropic_chat = gr.Chatbot(
                        label="Chat with Claude (TokenForge Enabled)",
                        height=500,
                        show_copy_button=True
                    )
                    anthropic_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Type your message here... TokenForge will automatically compress it!",
                        lines=3
                    )
                    with gr.Row():
                        anthropic_send = gr.Button("Send", variant="primary")
                        anthropic_clear = gr.Button("Clear Chat")
                
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Configuration")
                    anthropic_api_key = gr.Textbox(
                        label="Anthropic API Key",
                        type="password",
                        placeholder="sk-ant-... (or set ANTHROPIC_API_KEY env var)",
                        value=os.environ.get("ANTHROPIC_API_KEY", "")
                    )
                    anthropic_model = gr.Dropdown(
                        choices=[
                            "claude-sonnet-4-20250514",
                            "claude-3-5-sonnet-20241022",
                            "claude-3-opus-20240229",
                            "claude-3-sonnet-20240229"
                        ],
                        value="claude-sonnet-4-20250514",
                        label="Model"
                    )
                    anthropic_stats = gr.Markdown("### 📊 Statistics\n\n*Send a message to see compression stats*")
            
            anthropic_send.click(
                chat_anthropic,
                inputs=[anthropic_input, anthropic_chat, anthropic_api_key, anthropic_model],
                outputs=[anthropic_chat, anthropic_stats]
            )
            anthropic_input.submit(
                chat_anthropic,
                inputs=[anthropic_input, anthropic_chat, anthropic_api_key, anthropic_model],
                outputs=[anthropic_chat, anthropic_stats]
            )
            anthropic_clear.click(
                lambda: clear_chat("anthropic"),
                outputs=[anthropic_chat, anthropic_stats]
            )
        
        # Tab 3: Groq
        with gr.TabItem("⚡ Groq (Fast Inference)"):
            with gr.Row():
                with gr.Column(scale=2):
                    groq_chat = gr.Chatbot(
                        label="Chat with Groq (TokenForge Enabled)",
                        height=500,
                        show_copy_button=True
                    )
                    groq_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Type your message here... TokenForge will automatically compress it!",
                        lines=3
                    )
                    with gr.Row():
                        groq_send = gr.Button("Send", variant="primary")
                        groq_clear = gr.Button("Clear Chat")
                
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Configuration")
                    groq_api_key = gr.Textbox(
                        label="Groq API Key",
                        type="password",
                        placeholder="gsk_... (or set GROQ_API_KEY env var)",
                        value=os.environ.get("GROQ_API_KEY", "")
                    )
                    groq_model = gr.Dropdown(
                        choices=[
                            "llama-3.1-70b-versatile",
                            "llama-3.1-8b-instant",
                            "mixtral-8x7b-32768",
                            "gemma-7b-it"
                        ],
                        value="llama-3.1-70b-versatile",
                        label="Model"
                    )
                    groq_stats = gr.Markdown("### 📊 Statistics\n\n*Send a message to see compression stats*")
            
            groq_send.click(
                chat_groq,
                inputs=[groq_input, groq_chat, groq_api_key, groq_model],
                outputs=[groq_chat, groq_stats]
            )
            groq_input.submit(
                chat_groq,
                inputs=[groq_input, groq_chat, groq_api_key, groq_model],
                outputs=[groq_chat, groq_stats]
            )
            groq_clear.click(
                lambda: clear_chat("groq"),
                outputs=[groq_chat, groq_stats]
            )
        
        # Tab 4: Ollama
        with gr.TabItem("🦙 Ollama (Local)"):
            with gr.Row():
                with gr.Column(scale=2):
                    ollama_chat = gr.Chatbot(
                        label="Chat with Ollama (TokenForge Enabled)",
                        height=500,
                        show_copy_button=True
                    )
                    ollama_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Type your message here... TokenForge will automatically compress it!",
                        lines=3
                    )
                    with gr.Row():
                        ollama_send = gr.Button("Send", variant="primary")
                        ollama_clear = gr.Button("Clear Chat")
                
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Configuration")
                    gr.Markdown("**Note**: Make sure Ollama is running locally")
                    ollama_base_url = gr.Textbox(
                        label="Ollama Base URL",
                        value="http://localhost:11434/v1",
                        placeholder="http://localhost:11434/v1"
                    )
                    ollama_model = gr.Textbox(
                        label="Model Name",
                        value="llama3.2",
                        placeholder="llama3.2, mistral, etc."
                    )
                    ollama_stats = gr.Markdown("### 📊 Statistics\n\n*Send a message to see compression stats*")
            
            ollama_send.click(
                chat_ollama,
                inputs=[ollama_input, ollama_chat, ollama_base_url, ollama_model],
                outputs=[ollama_chat, ollama_stats]
            )
            ollama_input.submit(
                chat_ollama,
                inputs=[ollama_input, ollama_chat, ollama_base_url, ollama_model],
                outputs=[ollama_chat, ollama_stats]
            )
            ollama_clear.click(
                lambda: clear_chat("ollama"),
                outputs=[ollama_chat, ollama_stats]
            )
        
        # Tab 5: Generic
        with gr.TabItem("🔌 Generic API"):
            with gr.Row():
                with gr.Column(scale=2):
                    generic_chat = gr.Chatbot(
                        label="Chat with Generic OpenAI-Compatible API (TokenForge Enabled)",
                        height=500,
                        show_copy_button=True
                    )
                    generic_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Type your message here... TokenForge will automatically compress it!",
                        lines=3
                    )
                    with gr.Row():
                        generic_send = gr.Button("Send", variant="primary")
                        generic_clear = gr.Button("Clear Chat")
                
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Configuration")
                    gr.Markdown("**Works with**: LM Studio, vLLM, Together.ai, etc.")
                    generic_base_url = gr.Textbox(
                        label="API Base URL",
                        value="http://localhost:1234/v1",
                        placeholder="http://localhost:1234/v1"
                    )
                    generic_api_key = gr.Textbox(
                        label="API Key (optional)",
                        type="password",
                        placeholder="Leave empty if not needed"
                    )
                    generic_model = gr.Textbox(
                        label="Model Name",
                        value="default",
                        placeholder="Model identifier"
                    )
                    generic_stats = gr.Markdown("### 📊 Statistics\n\n*Send a message to see compression stats*")
            
            generic_send.click(
                chat_generic,
                inputs=[generic_input, generic_chat, generic_base_url, generic_api_key, generic_model],
                outputs=[generic_chat, generic_stats]
            )
            generic_input.submit(
                chat_generic,
                inputs=[generic_input, generic_chat, generic_base_url, generic_api_key, generic_model],
                outputs=[generic_chat, generic_stats]
            )
            generic_clear.click(
                lambda: clear_chat("generic"),
                outputs=[generic_chat, generic_stats]
            )
    
    # Footer
    gr.Markdown("""
    ---
    
    ### 🚀 About TokenForge
    
    TokenForge automatically compresses your messages using a dictionary-based compression system
    that LLMs can understand. This reduces token costs by **40-70%** while maintaining full functionality.
    
    **Features**:
    - ✅ Automatic compression (no code changes needed)
    - ✅ Privacy shield (PII detection and redaction)
    - ✅ Works with any LLM
    - ✅ Real-time cost savings tracking
    
    **[Learn More](https://github.com/tokenforge/tokenforge)** | **[PyPI Package](https://pypi.org/project/tokenforge/)**
    """)


if __name__ == "__main__":
    if not TOKENFORGE_AVAILABLE:
        print("ERROR: TokenForge is not available. Please install it:")
        print("  cd tokenforge && pip install -e .")
        sys.exit(1)
    
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)

