# GradioChat: How to Use Guide

This comprehensive guide explains how to use the GradioChat package to create customizable LLM-powered chat applications with Gradio. GradioChat provides a simple yet powerful framework for building chat interfaces that can connect to various language models.

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Configuration](#configuration)
4. [Creating a Chat Application](#creating-a-chat-application)
5. [Customization](#customization)
6. [API Reference](#api-reference)

## Installation

Install the package using pip:

```bash
pip install gradiochat
```

## Quick Start

Here's a minimal example to get you started:

```python
import gradiochat
from gradiochat.config import ModelConfig, ChatAppConfig
from pathlib import Path

# Create model configuration
model_config = ModelConfig(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    provider="huggingface",
    api_key_env_var="HF_API_KEY"  # Optional: Set in .env file or environment
)

# Create chat application configuration
config = ChatAppConfig(
    app_name="My Chat App",
    description="A simple chat application powered by Mistral",
    system_prompt="You are a helpful assistant.",
    model=model_config
)

# Create and launch the chat application
app = gradiochat.create_chat_app(config)
app.build_interface().launch()
```

## Configuration

The core of GradioChat is its configuration system which uses Pydantic for validation.

### ModelConfig

The `ModelConfig` class defines how to connect to a language model:

```python
from gradiochat.config import ModelConfig

# HuggingFace model
hf_model = ModelConfig(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    provider="huggingface",
    api_key_env_var="HF_API_KEY",  # Will read from environment variable
    api_base_url=None,  # Optional: Custom API endpoint
    max_tokens=1024,
    temperature=0.7
)
```

### Message

The `Message` class represents a single message in a conversation:

```python
from gradiochat.config import Message

# Create a system message
system_msg = Message(
    role="system",
    content="You are a helpful assistant."
)

# Create a user message
user_msg = Message(
    role="user",
    content="Hello, can you help me with Python?"
)

# Create an assistant message
assistant_msg = Message(
    role="assistant",
    content="Of course! I'd be happy to help with Python. What would you like to know?"
)
```

### ChatAppConfig

The `ChatAppConfig` class is the main configuration for your chat application:

```python
from gradiochat.config import ChatAppConfig, ModelConfig
from pathlib import Path

# Create model configuration
model_config = ModelConfig(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    provider="huggingface",
    api_key_env_var="HF_API_KEY"
)

# Create chat application configuration
config = ChatAppConfig(
    app_name="Python Helper",
    description="Get help with Python programming",
    system_prompt="You are a Python expert who helps users with programming questions.",
    starter_prompt="Hello! I'm your Python assistant. Ask me any Python-related question.",
    context_files=[Path("docs/python_tips.md")],  # Optional: Add context from files
    model=model_config,
    theme=None,  # Optional: Custom Gradio theme
    logo_path=Path("assets/logo.png"),  # Optional: Path to logo image
    show_system_prompt=True,  # Whether to show system prompt in UI
    show_context=True  # Whether to show context in UI
)
```

## Creating a Chat Application

### Basic Usage

The simplest way to create a chat application is using the `create_chat_app` function:

```python
import gradiochat
from gradiochat.config import ModelConfig, ChatAppConfig

# Create configurations
model_config = ModelConfig(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    provider="huggingface",
    api_key_env_var="HF_API_KEY"
)

config = ChatAppConfig(
    app_name="My Chat App",
    description="A simple chat application",
    system_prompt="You are a helpful assistant.",
    model=model_config
)

# Create and launch the app
app = gradiochat.create_chat_app(config)
app.build_interface().launch()
```

### Using Environment Variables

For API keys, it's recommended to use environment variables. You can create a `.env` file in your project root:

```
HF_API_KEY=your_huggingface_api_key_here
```

Then load it in your application:

```python
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Now create your ModelConfig with api_key_env_var
```

### Adding Context Files

You can provide additional context to your LLM by adding markdown files:

```python
from pathlib import Path

config = ChatAppConfig(
    # ... other parameters
    context_files=[
        Path("docs/product_info.md"),
        Path("docs/faq.md")
    ],
    # ... other parameters
)
```

## Customization

### Custom Themes

You can customize the appearance of your chat application using Gradio themes:

```python
import gradio as gr
from gradiochat.gradio_themes import create_theme

# Create a custom theme
my_theme = create_theme(
    primary_hue="blue",
    secondary_hue="purple",
    neutral_hue="gray"
)

# Use the theme in your config
config = ChatAppConfig(
    # ... other parameters
    theme=my_theme,
    # ... other parameters
)
```

### Advanced Theme Building

For more advanced theme customization, you can use the `gradio_themebuilder` module:

```python
from gradiochat.gradio_themebuilder import build_theme

# Create a fully customized theme
custom_theme = build_theme(
    primary_color="#3B82F6",
    secondary_color="#10B981",
    text_color="#1F2937",
    background_color="#F9FAFB",
    border_color="#E5E7EB"
)

# Use the theme in your config
config = ChatAppConfig(
    # ... other parameters
    theme=custom_theme,
    # ... other parameters
)
```

## API Reference

### BaseChatApp

The `BaseChatApp` class provides the core functionality for chat applications:

```python
from gradiochat.app import BaseChatApp
from gradiochat.config import ChatAppConfig

# Create configuration
config = ChatAppConfig(...)

# Create base app
base_app = BaseChatApp(config)

# Generate a response
response = base_app.generate_response("What is Python?")

# Generate a streaming response
for chunk in base_app.generate_stream("Tell me about Python"):
    print(chunk, end="", flush=True)
```

### GradioChat

The `GradioChat` class provides the Gradio UI for the chat application:

```python
from gradiochat.ui import GradioChat
from gradiochat.app import BaseChatApp

# Create base app
base_app = BaseChatApp(config)

# Create Gradio interface
gradio_app = GradioChat(base_app)

# Build and launch the interface
interface = gradio_app.build_interface()
interface.launch()
```

### LLM Clients

The package currently supports HuggingFace models through the `HuggingFaceClient` class:

```python
from gradiochat.app import HuggingFaceClient
from gradiochat.config import ModelConfig, Message

# Create model config
model_config = ModelConfig(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    provider="huggingface",
    api_key_env_var="HF_API_KEY"
)

# Create client
client = HuggingFaceClient(model_config)

# Generate a completion
messages = [
    Message(role="system", content="You are a helpful assistant."),
    Message(role="user", content="What is Python?")
]
response = client.chat_completion(messages)
```

## Complete Example

Here's a complete example that demonstrates most features:

```python
import gradio as gr
from gradiochat.config import ModelConfig, ChatAppConfig
from gradiochat.gradio_themes import create_theme
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a custom theme
theme = create_theme(primary_hue="blue", secondary_hue="indigo")

# Create model configuration
model_config = ModelConfig(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    provider="huggingface",
    api_key_env_var="HF_API_KEY",
    max_tokens=2048,
    temperature=0.8
)

# Create chat application configuration
config = ChatAppConfig(
    app_name="Python Expert",
    description="Get expert help with Python programming",
    system_prompt="You are a Python expert who helps users with programming questions. Provide clear, concise, and accurate information.",
    starter_prompt="Hello! I'm your Python assistant. How can I help you today?",
    context_files=[Path("docs/python_reference.md")],
    model=model_config,
    theme=theme,
    logo_path=Path("assets/python_logo.png"),
    show_system_prompt=True,
    show_context=True
)

# Create and launch the chat application
import gradiochat
app = gradiochat.create_chat_app(config)
app.build_interface().launch(share=True)
```
