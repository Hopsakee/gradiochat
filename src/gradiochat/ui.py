"""Gradio interface for the chat application."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/02_ui.ipynb.

# %% auto 0
__all__ = ['GradioChat', 'create_chat_app']

# %% ../../nbs/02_ui.ipynb 3
import gradio as gr
from typing import List, Tuple, Generator, Dict, Any, Optional
from .config import ChatAppConfig, ModelConfig
from .app import BaseChatApp
from pathlib import Path

# %% ../../nbs/02_ui.ipynb 4
class GradioChat:
    """Gradio interface for the chat application"""
    
    def __init__(self, app: BaseChatApp):
        """Initialize with a configured BaseChatApp"""
        self.app = app
        self.interface = None
    
    def respond(self, message: str, chat_history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
        """Generate a response to the user message and update chat history"""
        # Store the current chat history in the app
        self.app.chat_history = chat_history
        
        # Generate response
        response = self.app.generate_response(message)
        
        # Update chat history
        chat_history.append((message, response))
        
        # Return empty message (to clear input) and updated history
        return "", chat_history
    
    def respond_stream(self, message: str, chat_history: List[Tuple[str, str]]) -> Generator[Tuple[str, List[Tuple[str, str]]], None, None]:
        """Generate a streaming response to the user message"""
        # Store the current chat history in the app
        self.app.chat_history = chat_history
        
        # Add user message to history with empty assistant response
        chat_history.append((message, ""))
        
        # Stream the response
        accumulated_text = ""
        for text_chunk in self.app.generate_stream(message):
            accumulated_text += text_chunk
            
            # Update the last assistant message
            updated_history = chat_history[:-1] + [(message, accumulated_text)]
            
            # Yield empty message and updated history
            yield "", updated_history
    
    def build_interface(self) -> gr.Blocks:
        """Build and return the Gradio interface"""
        with gr.Blocks(theme=self.app.config.theme) as interface:
            with gr.Row():
                # Left column for logo
                with gr.Column(scale=1):
                    if self.app.config.logo_path:
                        gr.Image(value=self.app.config.logo_path,
                            show_label=False,
                            container=False,
                            show_download_button=False,
                            show_fullscreen_button=False,
                            height=80,
                            width=80)
                    else:
                        gr.Image(value=None,
                            show_label=False,
                            container=False,
                            show_download_button=False,
                            show_fullscreen_button=False,
                            height=80,
                            width=80)
                with gr.Column(scale=4):
                    # App title and description
                    gr.Markdown(f"# {self.app.config.app_name}")
                    if self.app.config.description:
                        gr.Markdown(self.app.config.description)
            
            # Chat interface
            chatbot = gr.Chatbot(
                height=500,
                label="Conversation",
                editable=True,
                show_copy_button=True,
                show_copy_all_button=True)
            msg = gr.Textbox(
                placeholder="Type your message here...",
                label="Your message",
                lines=2
            )
            
            # Buttons
            with gr.Row():
                submit_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.ClearButton([msg, chatbot], value="Clear chat")

            # Export functionality
            with gr.Accordion("Export Options", open=False):
                export_md = gr.Markdown("Select export options:")
                
                with gr.Row():
                    export_last_btn = gr.Button("Export Last Response")
                    export_all_btn = gr.Button("Export Full Conversation")
                
                # Hidden textbox to hold the markdown for export
                export_text = gr.Textbox(visible=False)
                
                # Buttons for copying and downloading
                with gr.Row():
                    copy_btn = gr.Button("Copy to Clipboard")
                    download_btn = gr.Button("Download as Markdown")
                
                file_output = gr.File(label="Download", visible=False)
            
            # System prompt and context viewer (collapsible)
            with gr.Accordion("View System Information", open=False):
                if self.app.config.show_system_prompt:
                    gr.Markdown(f"### System Prompt\n{self.app.config.system_prompt}")
                
                if self.app.config.show_context and hasattr(self.app, 'context_text') and self.app.context_text:
                    gr.Markdown(f"### Additional Context\n{self.app.context_text}")
            
            # Set up event handlers
            submit_btn.click(
                self.respond,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            msg.submit(
                self.respond,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )

             # Export event handlers
            def format_last_response(chat_history):
                if not chat_history:
                    return "No conversation to export."
                last_user_msg, last_assistant_msg = chat_history[-1]
                return f"# Response\n\n{last_assistant_msg}"
            
            def format_full_conversation(chat_history):
                if not chat_history:
                    return "No conversation to export."
                
                markdown = f"# {self.app.config.app_name} - Conversation\n\n"
                
                for user_msg, assistant_msg in chat_history:
                    markdown += f"## User\n\n{user_msg}\n\n"
                    markdown += f"## Assistant\n\n{assistant_msg}\n\n"
                    markdown += "---\n\n"
                
                return markdown
            
            export_last_btn.click(
                format_last_response,
                inputs=[chatbot],
                outputs=[export_text]
            )
            
            export_all_btn.click(
                format_full_conversation,
                inputs=[chatbot],
                outputs=[export_text]
            )
            
            # File download functionality
            def create_markdown_file(markdown_text):
                return [f"{self.app.config.app_name.replace(' ', '_')}_export.md",
                    markdown_text]
            
            download_btn.click(
                lambda text: [f"{self.app.config.app_name.replace(' ','_')}._export.md", text],
                inputs=[export_text],
                outputs=[file_output]
            )
                
            # Initialize with starter prompt if available
            if self.app.config.starter_prompt:
                chatbot.value = [("", self.app.config.starter_prompt)]
            
            self.interface = interface
            return interface
    
    def launch(self, **kwargs):
        """Launch the Gradio interface"""
        if self.interface is None:
            self.build_interface()
        
        return self.interface.launch(**kwargs)

# %% ../../nbs/02_ui.ipynb 5
def create_chat_app(config: ChatAppConfig) -> GradioChat:
    """Create a complete chat application from a configuration"""
    base_app = BaseChatApp(config)
    return GradioChat(base_app)
