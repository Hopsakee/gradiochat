"""Contains BaseChatApp and large language model integration logic. Implements the core functionality indepent of the UI."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/01_app.ipynb.

# %% auto 0
__all__ = ['LLMClientProtocol', 'HuggingFaceClient', 'TogetherAiClient', 'create_llm_client', 'BaseChatApp']

# %% ../../nbs/01_app.ipynb 3
from typing import Protocol, runtime_checkable, Generator, List
from openai import OpenAI

from .config import ModelConfig, Message, ChatAppConfig
from .utils import *

# %% ../../nbs/01_app.ipynb 7
@runtime_checkable
class LLMClientProtocol(Protocol):
    """Protocol defining the interface for LLM clients"""
    
    def chat_completion(self, messages: List[Message], **kwargs) -> str:
        """Generate a response from the LLM"""
        ...
    
    def chat_completion_stream(self, messages: List[Message], **kwargs) -> Generator[str, None, None]:
        """Generate a streaming response from the LLM"""
        ...

# %% ../../nbs/01_app.ipynb 9
class HuggingFaceClient():
    """Client for interacting with HuggingFace models"""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize the client with model configuration"""
        self.model_config = model_config

        # Default to HF Inference API if no base URL is provided
        base_url = model_config.api_base_url or "https://router.huggingface.co/hf-inference/v1"

        self.client = OpenAI(
            base_url=base_url,
            api_key=model_config.api_key or "hf_no_api_key_provided"
        )
    
    def chat_completion(self, 
            messages: List[Message], # List of messages conforming to the Message pydantic dataclass
            **kwargs
            ) -> str:
        """Generate a chat completion from the HuggingFace model"""
        # Convert our Message objects to the format expected by the OpenAI client
        openai_messages = [{"role": msg.role, "content": msg.content} for msg in messages]

        completion = self.client.chat.completions.create(
            model=self.model_config.model_name,
            messages=openai_messages,
            max_completion_tokens=kwargs.get("max_completion_tokens", self.model_config.max_completion_tokens),
            temperature=kwargs.get("temperature", self.model_config.temperature)
        )

        # Extract the generated text
        return completion.choices[0].message.content
    
    def chat_completion_stream(self, messages: List[Message], **kwargs) -> Generator[str, None, None]:
        """Generate a streaming chat completion"""
        # For now, use non-streaming version as a placeholder
        # We'll implement proper streaming later
        result = self.chat_completion(messages, **kwargs)
        yield result

# %% ../../nbs/01_app.ipynb 10
class TogetherAiClient():
    """Client for interacting with models through the TogetherAI API server
    We use the openai package"""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize the client with model configuration"""
        self.model_config = model_config

        self.client = OpenAI(
            base_url=model_config.api_base_url or "https://api.together.xyz/v1", # Default to Together AI Inference API if no base URL is provided
            api_key=model_config.api_key,
        )
    
    def chat_completion(self, 
            messages: List[Message], # List of messages conforming to the Message pydantic dataclass
            **kwargs
            ) -> str:
        """Generate a chat completion from the Together AI API"""
        # Convert our Message objects to the format expected by the OpenAI client
        openai_messages = [{"role": msg.role, "content": msg.content} for msg in messages]

        completion = self.client.chat.completions.create(
            model=self.model_config.model_name,
            messages=openai_messages,
            max_completion_tokens=kwargs.get("max_completion_tokens", self.model_config.max_completion_tokens),
            temperature=kwargs.get("temperature", self.model_config.temperature),
            top_p=kwargs.get("top_p", self.model_config.top_p),
            stop=kwargs.get("stop", self.model_config.stop) or ["<|eot_id|>","<|eom_id|>"]
        )

        # Extract the generated text
        return completion.choices[0].message.content
    
    def chat_completion_stream(self,
            messages: List[Message], # List of messages conforming to the Message pydantic dataclass
            **kwargs) -> Generator[str, None, None]:
        """Generate a streaming chat completion"""

        stream = self.client.chat.completions.create(
            model=self.model_config.model_name,
            messages=openai_messages,
            max_completion_tokens=kwargs.get("max_completion_tokens", self.model_config.max_completion_tokens),
            temperature=kwargs.get("temperature", self.model_config.temperature),
            top_p=kwargs.get("top_p", self.model_config.top_p),
            stop=kwargs.get("stop", self.model_config.stop) or ["<|eot_id|>","<|eom_id|>"],
            stream=True
        )

        for token in stream:
            if hasattr(token, 'choices') and token.choices[0].delta.content is not None:
                yield token.choices[0].delta.content
           

# %% ../../nbs/01_app.ipynb 12
def create_llm_client(model_config: ModelConfig) -> LLMClientProtocol:
    """
    Factory function to create an LLM client based on the provider.
    """
    if model_config.provider.lower() == "huggingface":
        return HuggingFaceClient(model_config)
    if model_config.provider.lower() == "togetherai":
        return TogetherAiClient(model_config)
    else:
        raise ValueError(f"Unsupported provider: {model_config.provider}")

# %% ../../nbs/01_app.ipynb 14
class BaseChatApp:
    """Base class for creating configurable chat applications with Gradio"""
    
    def __init__(self, config: ChatAppConfig):
        """Initialize the chat application"""
        self.config = config
        self.chat_history = []
        self._load_context()
        self.client = create_llm_client(config.model)
        
    def _load_context(self) -> None:
        """Load context from markdown files"""
        self.context_text = ""
        for file_path in self.config.context_files:
            if file_path.exists() and file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.context_text += f.read() + "\n\n"
    
    def prepare_messages(self, user_message: str) -> List[Message]:
        """Prepare the messages for the LLM, including system prompt and chat history"""
        messages = []
        
        # Add system message with prompt and context
        system_content = self.config.system_prompt
        if self.context_text:
            system_content += f"\n\nAdditional information: {self.context_text}"
        
        messages.append(Message(role="system", content=system_content))
        
        # Add chat history
        for user_msg, assistant_msg in self.chat_history:
            messages.append(Message(role="user", content=user_msg))
            messages.append(Message(role="assistant", content=assistant_msg))
        
        # Add current user message
        messages.append(Message(role="user", content=user_message))
        
        return messages
    
    def generate_response(self, user_message: str, **kwargs) -> str:
        """Generate a response to the user message"""
        messages = self.prepare_messages(user_message)
        return self.client.chat_completion(messages, **kwargs)
    
    def generate_stream(self, user_message: str, **kwargs) -> Generator[str, None, None]:
        """Generate a streaming response to the user message"""
        messages = self.prepare_messages(user_message)
        return self.client.chat_completion_stream(messages, **kwargs)
