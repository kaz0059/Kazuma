import gradio as gr


def launch_gui(brain, persona, memory):
    # Seed previous session into chat window
    initial_history = memory.load_history_pairs(max_messages=None) if memory.enabled else []

    with gr.Blocks(title=f"{persona.name} – Your AI") as demo:
        gr.Markdown(f"# {persona.name} — Your AI Assistant")
        with gr.Row():
            style_dd = gr.Dropdown(
                ["casual", "concise", "playful", "formal"],
                value=persona.style,
                label="Style",
            )
            mood_dd = gr.Dropdown(
                ["friendly", "neutral", "serious", "cheerful"],
                value=persona.mood,
                label="Mood",
            )
            name_tb = gr.Textbox(value=persona.name, label="Name", scale=1)

        chat = gr.Chatbot(value=initial_history, height=520)
        msg = gr.Textbox(placeholder="Type a message and press Enter…", label="Message")

        with gr.Row():
            send_btn = gr.Button("Send", variant="primary")
            clear_btn = gr.Button("Clear Chat (backup first)")

        status = gr.Markdown("")

        def on_persona_change(style, mood, name):
            persona.update("style", style)
            persona.update("mood", mood)
            persona.update("name", name)
            return gr.update(value=f"**Persona saved.** Name: {persona.name}, Style: {persona.style}, Mood: {persona.mood}")

        def respond(message, history):
            if not message.strip():
                return history, ""
            reply = brain.think(message)
            history = history + [(message, reply)]
            return history, ""

        def clear_chat():
            path = memory.backup_log()
            # reset the chatbot display
            return [], f"Backed up the previous conversation to: `{path or 'n/a'}` and cleared the current log."

        style_dd.change(on_persona_change, [style_dd, mood_dd, name_tb], [status])
        mood_dd.change(on_persona_change, [style_dd, mood_dd, name_tb], [status])
        name_tb.submit(on_persona_change, [style_dd, mood_dd, name_tb], [status])

        msg.submit(respond, [msg, chat], [chat, msg])
        send_btn.click(respond, [msg, chat], [chat, msg])
        clear_btn.click(clear_chat, [], [chat, status])

    demo.launch(server_name="127.0.0.1", server_port=7860)
