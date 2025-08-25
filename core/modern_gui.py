# core/gui.py

import gradio as gr
import time
import os
from datetime import datetime
from typing import List, Dict


def create_modern_gui(brain, memory):
    """Create a premium LobeChat-style interface without persona system."""
    
    # Premium CSS styling
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --glass-bg: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.12);
        --dark-bg: #0a0a0f;
        --dark-surface: #151520;
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.7);
        --text-muted: rgba(255, 255, 255, 0.5);
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .gradio-container {
        height: 100vh !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: var(--dark-bg) !important;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.15) 0%, transparent 50%);
        display: flex !important;
        flex-direction: column !important;
    }
    
    .header {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(24px) !important;
        border-bottom: 1px solid var(--glass-border) !important;
        padding: 20px 32px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
    
    .title {
        font-size: 24px !important;
        font-weight: 700 !important;
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    .chat-container {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        max-width: 900px !important;
        margin: 0 auto !important;
        width: 100% !important;
        padding: 24px !important;
    }
    
    .input-section {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(24px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 24px !important;
        padding: 8px !important;
        margin-top: 20px !important;
    }
    
    .send-btn {
        background: var(--primary-gradient) !important;
        border: none !important;
        border-radius: 16px !important;
        color: white !important;
        padding: 12px 16px !important;
        transition: transform 0.2s !important;
    }
    
    .send-btn:hover {
        transform: scale(1.05) !important;
    }
    
    .control-btn {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: var(--text-secondary) !important;
        padding: 12px 20px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .control-btn:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: var(--text-primary) !important;
    }
    
    .status {
        background: rgba(0, 255, 136, 0.1) !important;
        border: 1px solid rgba(0, 255, 136, 0.2) !important;
        color: #00ff88 !important;
        padding: 16px 24px !important;
        border-radius: 16px !important;
        text-align: center !important;
        margin: 16px 0 !important;
    }
    
    /* Hide Gradio defaults */
    .gradio-container .wrap,
    .gradio-container .contain {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    """

    def respond_with_typing(message, history):
        """Generate response with typing effect."""
        if not message.strip():
            return history, ""
        
        # Add user message
        history = history + [{"role": "user", "content": message}]
        yield history, ""
        
        # Brief pause for premium feel
        time.sleep(0.3)
        
        # Get AI response
        try:
            ai_response = brain.think(message)
        except Exception as e:
            ai_response = f"I encountered an error: {str(e)}"
        
        # Add AI response
        history = history + [{"role": "assistant", "content": ai_response}]
        yield history, ""

    def clear_conversation():
        """Clear chat and create backup."""
        try:
            if memory and memory.enabled:
                backup_path = memory.backup_log()
                if backup_path:
                    return [], "✨ Conversation cleared and backed up"
                else:
                    return [], "✨ Conversation cleared (no previous messages)"
            else:
                return [], "✨ Conversation cleared"
        except Exception as e:
            return [], f"❌ Error: {str(e)}"

    def export_conversation(history):
        """Export conversation to markdown file."""
        try:
            if not history:
                return "📝 No conversation to export"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_conversation_{timestamp}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# 🤖 AI Assistant Conversation\n\n")
                f.write(f"**Exported:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n\n")
                f.write("---\n\n")
                
                for msg in history:
                    role = msg.get("role", "")
                    content = msg.get("content", "")
                    
                    if role == "user":
                        f.write(f"## 👤 You\n\n{content}\n\n")
                    elif role == "assistant":
                        f.write(f"## 🤖 Assistant\n\n{content}\n\n---\n\n")
            
            return f"📁 Exported to {filename}"
        except Exception as e:
            return f"❌ Export failed: {str(e)}"

    def get_memory_stats():
        """Get current memory statistics."""
        if memory and memory.enabled:
            stats = memory.get_stats()
            return f"📊 Memory: {stats['total_messages']} messages, {stats['size']}"
        else:
            return "ℹ️ Memory is disabled"

    # Load existing history
    initial_history = []
    try:
        if memory and memory.enabled:
            initial_history = memory.load_history_messages(max_messages=50)
    except Exception as e:
        print(f"Could not load history: {e}")

    # Create interface
    with gr.Blocks(css=css, title="🚀 AI Assistant") as demo:
        
        # Header
        gr.HTML("""
        <div class="header">
            <div class="title">🤖 AI Assistant</div>
            <div style="color: var(--text-secondary);">Smart AI Experience</div>
        </div>
        """)
        
        # Status display
        status = gr.HTML("", visible=False, elem_classes="status")
        
        # Main chat interface
        with gr.Column(elem_classes="chat-container"):
            chatbot = gr.Chatbot(
                type='messages',
                value=initial_history,
                height="60vh",
                show_label=False,
                container=False,
                show_copy_button=True,
                show_share_button=False,
                bubble_full_width=False
            )
            
            # Input section
            with gr.Row(elem_classes="input-section"):
                msg = gr.Textbox(
                    placeholder="Type your message here... ✨",
                    show_label=False,
                    lines=1,
                    max_lines=6,
                    container=False,
                    scale=4
                )
                send_btn = gr.Button("🚀 Send", elem_classes="send-btn", scale=1)
            
            # Controls
            with gr.Row():
                clear_btn = gr.Button("🗑️ Clear", elem_classes="control-btn")
                export_btn = gr.Button("📥 Export", elem_classes="control-btn")
                stats_btn = gr.Button("📊 Stats", elem_classes="control-btn")

        # Event handlers
        msg.submit(respond_with_typing, [msg, chatbot], [chatbot, msg])
        send_btn.click(respond_with_typing, [msg, chatbot], [chatbot, msg])
        
        clear_btn.click(clear_conversation, outputs=[chatbot, status]).then(
            lambda: gr.update(visible=True), outputs=[status]
        ).then(
            lambda: gr.update(visible=False), outputs=[status], show_progress=False
        )
        
        export_btn.click(export_conversation, [chatbot], [status]).then(
            lambda: gr.update(visible=True), outputs=[status]
        ).then(
            lambda: gr.update(visible=False), outputs=[status], show_progress=False
        )
        
        stats_btn.click(get_memory_stats, outputs=[status]).then(
            lambda: gr.update(visible=True), outputs=[status]
        ).then(
            lambda: gr.update(visible=False), outputs=[status], show_progress=False
        )

    return demo


def launch_modern_gui(brain, memory):
    """Launch the premium GUI interface."""
    demo = create_modern_gui(brain, memory)
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        quiet=True,
        inbrowser=True,
        show_error=True
    )