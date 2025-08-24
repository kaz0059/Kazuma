# modern_gui.py

import gradio as gr
import time
from datetime import datetime


def create_modern_gui(brain, memory):
    """Create a premium LobeChat-style interface"""
    
    # Premium LobeChat-inspired CSS
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --glass-bg: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.12);
        --dark-bg: #0a0a0f;
        --dark-surface: #151520;
        --premium-purple: #7c3aed;
        --premium-blue: #3b82f6;
        --premium-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
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
    
    html, body {
        height: 100%;
        overflow: hidden;
    }
    
    /* Main Container - Premium Dark Theme */
    .gradio-container {
        height: 100vh !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: var(--dark-bg) !important;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(124, 58, 237, 0.1) 0%, transparent 50%) !important;
        display: flex !important;
        flex-direction: column !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    /* Animated Background Particles */
    .gradio-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, rgba(255, 255, 255, 0.15), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(102, 126, 234, 0.3), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(118, 75, 162, 0.25), transparent);
        background-repeat: repeat;
        background-size: 120px 120px;
        animation: float 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-10px) rotate(1deg); }
        66% { transform: translateY(5px) rotate(-1deg); }
    }
    
    /* Header - Glass Morphism */
    .lobe-header {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-bottom: 1px solid var(--glass-border) !important;
        padding: 20px 32px !important;
        position: relative !important;
        z-index: 10 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
    
    .lobe-title {
        font-size: 24px !important;
        font-weight: 700 !important;
        background: var(--premium-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        letter-spacing: -0.5px !important;
    }
    
    .lobe-subtitle {
        color: var(--text-secondary) !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        opacity: 0.8 !important;
    }
    
    .status-indicator {
        width: 8px !important;
        height: 8px !important;
        background: #00ff88 !important;
        border-radius: 50% !important;
        animation: pulse-glow 2s ease-in-out infinite !important;
        box-shadow: 0 0 12px #00ff88 !important;
    }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    /* Chat Container - Premium Layout */
    .lobe-chat-container {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        position: relative !important;
        z-index: 5 !important;
        max-width: 900px !important;
        margin: 0 auto !important;
        width: 100% !important;
        padding: 0 24px !important;
        overflow: hidden !important;
    }
    
    .lobe-chat-area {
        flex: 1 !important;
        overflow-y: auto !important;
        padding: 32px 0 !important;
        scroll-behavior: smooth !important;
    }
    
    /* Message Bubbles - Premium Design */
    .message-container {
        margin: 24px 0 !important;
        animation: slideUp 0.5s ease-out !important;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message-bubble {
        max-width: 85% !important;
        padding: 20px 24px !important;
        border-radius: 24px !important;
        position: relative !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        line-height: 1.6 !important;
        font-size: 15px !important;
        font-weight: 400 !important;
        border: 1px solid var(--glass-border) !important;
        transition: all 0.3s ease !important;
    }
    
    .message-bubble:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4) !important;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2)) !important;
        color: var(--text-primary) !important;
        margin-left: auto !important;
        border-bottom-right-radius: 8px !important;
    }
    
    .assistant-message {
        background: rgba(255, 255, 255, 0.05) !important;
        color: var(--text-primary) !important;
        margin-right: auto !important;
        border-bottom-left-radius: 8px !important;
    }
    
    /* Input Area - Premium Glass Design */
    .lobe-input-section {
        padding: 32px 0 !important;
        position: relative !important;
        z-index: 10 !important;
    }
    
    .lobe-input-container {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 24px !important;
        padding: 8px !important;
        display: flex !important;
        align-items: flex-end !important;
        gap: 12px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .lobe-input-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .lobe-input-container:focus-within {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.3), 0 8px 32px rgba(102, 126, 234, 0.2) !important;
    }
    
    .lobe-input-container:focus-within::before {
        left: 100%;
    }
    
    .lobe-input {
        flex: 1 !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        padding: 16px 20px !important;
        color: var(--text-primary) !important;
        font-size: 16px !important;
        font-weight: 400 !important;
        line-height: 1.5 !important;
        resize: none !important;
        min-height: 24px !important;
        max-height: 120px !important;
        font-family: inherit !important;
    }
    
    .lobe-input::placeholder {
        color: var(--text-muted) !important;
        font-weight: 400 !important;
    }
    
    /* Send Button - Premium Animated */
    .lobe-send-btn {
        width: 48px !important;
        height: 48px !important;
        border-radius: 16px !important;
        border: none !important;
        background: var(--premium-gradient) !important;
        color: white !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        font-size: 20px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
    }
    
    .lobe-send-btn::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transition: all 0.3s ease;
        transform: translate(-50%, -50%);
    }
    
    .lobe-send-btn:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
    }
    
    .lobe-send-btn:hover::before {
        width: 100%;
        height: 100%;
    }
    
    .lobe-send-btn:active {
        transform: scale(0.95) !important;
    }
    
    .lobe-send-btn:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }
    
    /* Control Buttons - Subtle Premium */
    .lobe-controls {
        display: flex !important;
        gap: 16px !important;
        justify-content: center !important;
        margin-top: 24px !important;
    }
    
    .lobe-control-btn {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: var(--text-secondary) !important;
        padding: 12px 20px !important;
        border-radius: 12px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .lobe-control-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        transition: left 0.5s ease;
    }
    
    .lobe-control-btn:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
        color: var(--text-primary) !important;
        transform: translateY(-2px) !important;
    }
    
    .lobe-control-btn:hover::before {
        left: 100%;
    }
    
    /* Status Messages */
    .lobe-status {
        background: rgba(0, 255, 136, 0.1) !important;
        border: 1px solid rgba(0, 255, 136, 0.2) !important;
        color: #00ff88 !important;
        padding: 16px 24px !important;
        border-radius: 16px !important;
        text-align: center !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        margin: 16px 0 !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        animation: fadeInScale 0.5s ease-out !important;
    }
    
    @keyframes fadeInScale {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.5), rgba(118, 75, 162, 0.5));
        border-radius: 4px;
        border: 2px solid transparent;
        background-clip: content-box;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
        background-clip: content-box;
    }
    
    /* Hide Gradio Defaults */
    .gradio-container .wrap,
    .gradio-container .contain {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .lobe-header {
            padding: 16px 20px !important;
        }
        
        .lobe-title {
            font-size: 20px !important;
        }
        
        .lobe-chat-container {
            padding: 0 16px !important;
        }
        
        .message-bubble {
            max-width: 92% !important;
            padding: 16px 20px !important;
        }
        
        .lobe-input-section {
            padding: 20px 0 !important;
        }
    }
    """

    def convert_to_messages_format(history_pairs):
        """Convert tuple-based history to messages format"""
        messages = []
        for user_msg, ai_msg in history_pairs:
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if ai_msg:
                messages.append({"role": "assistant", "content": ai_msg})
        return messages

    def respond_with_typing(message, history):
        """Generate response with smooth animation"""
        if not message.strip():
            return history, ""
        
        # Add user message
        history = history + [{"role": "user", "content": message}]
        yield history, ""
        
        # Brief pause for premium feel
        time.sleep(0.6)
        
        # Get AI response
        try:
            ai_response = brain.think(message)
        except Exception as e:
            ai_response = f"I encountered an error: {str(e)}"
        
        # Add AI response
        history = history + [{"role": "assistant", "content": ai_response}]
        yield history, ""

    def clear_conversation():
        """Clear chat with premium feedback"""
        try:
            if memory and memory.enabled:
                memory.backup_log()
            return [], "✨ Conversation cleared successfully"
        except Exception as e:
            return [], f"❌ Error: {str(e)}"

    def export_conversation(history):
        """Export with premium styling"""
        try:
            if not history:
                return "📝 No conversation to export"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"lobe_chat_export_{timestamp}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# 🤖 AI Assistant Conversation\n\n")
                f.write(f"**Exported:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n\n")
                f.write("---\n\n")
                
                for i, msg in enumerate(history):
                    role = msg.get("role", "")
                    content = msg.get("content", "")
                    
                    if role == "user":
                        f.write(f"## 👤 You\n\n{content}\n\n")
                    elif role == "assistant":
                        f.write(f"## 🤖 Assistant\n\n{content}\n\n")
                        if i < len(history) - 1:
                            f.write("---\n\n")
            
            return f"📁 Exported to {filename}"
        except Exception as e:
            return f"❌ Export failed: {str(e)}"

    # Load existing history
    initial_history = []
    try:
        if memory and memory.enabled:
            history_pairs = memory.load_history_pairs(max_messages=50)
            initial_history = convert_to_messages_format(history_pairs)
    except Exception as e:
        print(f"Could not load history: {e}")

    # Create premium interface
    with gr.Blocks(css=css, title="🚀 AI Assistant", theme=gr.themes.Glass()) as demo:
        
        # Premium Header
        gr.HTML("""
        <div class="lobe-header">
            <div>
                <div class="lobe-title">✨ AI Assistant</div>
                <div class="lobe-subtitle">Premium AI Experience</div>
            </div>
            <div class="status-indicator"></div>
        </div>
        """)
        
        # Main Chat Container
        with gr.Column(elem_classes="lobe-chat-container"):
            
            # Status messages
            status = gr.HTML("", elem_classes="lobe-status", visible=False)
            
            # Chat Interface
            with gr.Column(elem_classes="lobe-chat-area"):
                chatbot = gr.Chatbot(
                    type='messages',
                    value=initial_history,
                    height="55vh",
                    show_label=False,
                    container=False,
                    show_copy_button=False,
                    show_share_button=False,
                    avatar_images=None,
                    bubble_full_width=False,
                    layout="panel",
                    elem_classes="premium-chat"
                )
            
            # Premium Input Section
            with gr.Column(elem_classes="lobe-input-section"):
                with gr.Row(elem_classes="lobe-input-container"):
                    msg = gr.Textbox(
                        placeholder="Type your message here... ✨",
                        show_label=False,
                        lines=1,
                        max_lines=6,
                        elem_classes="lobe-input",
                        container=False
                    )
                    send_btn = gr.Button("🚀", elem_classes="lobe-send-btn")
                
                # Control Buttons
                with gr.Row(elem_classes="lobe-controls"):
                    clear_btn = gr.Button("🗑️ Clear", elem_classes="lobe-control-btn")
                    export_btn = gr.Button("📥 Export", elem_classes="lobe-control-btn")

        # Event Handlers
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

    return demo


def launch_modern_gui(brain, memory):
    """Launch the premium LobeChat-style GUI"""
    demo = create_modern_gui(brain, memory)
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        quiet=True,
        inbrowser=True,
        show_error=True
    )