"""Define the data classes using Pydantic, making it possible to configure the chat application and do input validation."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/00_config.ipynb.

# %% auto 0
__all__ = ['ModelConfig', 'Message', 'ChatAppConfig']

# %% ../../nbs/00_config.ipynb 3
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple, Literal, Any
import os
import gradio as gr
from pathlib import Path
from dotenv import load_dotenv

# %% ../../nbs/00_config.ipynb 8
class ModelConfig(BaseModel):
    """Configuration for the LLM model"""
    model_name: str = Field(..., description="Name or path of the model to use")
    provider: str = Field(default="huggingface", description="Model provider (huggingface, openai, etc)")
    api_key_env_var: Optional[str] = Field(default=None, description="Environment variable name for API key")
    api_base_url: Optional[str] = Field(default=None, description="Base URL for API reqeuest")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_completion_tokens: int = Field(default=1024, description="Maximum tokens to generate")
    top_p: float = Field(default=0.7, description="Adjust the number of choices for each predicted token [0-1]")
    top_k: int = Field(default=50, description="Limits the number of choices for the next predicted token. Not available for OpenAI API")
    frequency_penalty: float = Field(default=0, description="Reduces the likelihood of repeating prompt text or getting stuck in a loop [-2 -> 2]")
    stop: Optional[List[str]] = Field(default=["\nUser:", "<|endoftext|>"], description="Sequences to stop generation")
    stream: Optional[bool] = Field(default=None, description="If set to true, the model response data will be streamed to the client as it is generated using server-sent events.")

    
    @property
    def api_key(self) -> Optional[str]:
        """Get the API key from environment variables if specified"""
        if self.api_key_env_var:
            if os.environ.get(self.api_key_env_var):
                return os.environ.get(self.api_key_env_var)
            raise ValueError(f"The environment variable {self.api_key_env_var} is not found in the .env file.")
        return None

# %% ../../nbs/00_config.ipynb 11
class Message(BaseModel):
    """A message in a conversation"""
    role: Literal["system", "user", "assistant"] = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")

# %% ../../nbs/00_config.ipynb 14
class ChatAppConfig(BaseModel):
    """Main configuration for a chat application"""
    app_name: str = Field(..., description="Name of the application")
    description: str = Field(default="", description="Description of the application")
    system_prompt: str = Field(..., description="System prompt for the LLM")
    starter_prompt: Optional[str] = Field(default=None, description="Initial prompt to start the conversation")
    context_files: List[Path] = Field(default=[], description="List of markdown files for additional context")
    model: ModelConfig
    theme: Optional[Any] = Field(default=None, description="Gradio theme to use")
    logo_path: Optional[Path] = Field(default=None, description="Path to logo image")
    show_system_prompt: bool = Field(default=True, description="Whether to show system prompt in UI")
    show_context: bool = Field(default=True, description="Whether to show context in UI")
