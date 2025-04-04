"""Some functions to help with development"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/97_gradiochat_utils.ipynb.

# %% auto 0
__all__ = ['pydantic_to_markdown_table']

# %% ../../nbs/97_gradiochat_utils.ipynb 3
import inspect
from typing import Type, Any, Optional, Union, get_type_hints, get_origin, get_args
from pydantic import BaseModel, Field
from IPython.display import Markdown, display

# %% ../../nbs/97_gradiochat_utils.ipynb 4
def pydantic_to_markdown_table(model_class: Type[BaseModel]) -> None:
    """
    Convert a Pydantic model class to a markdown table and display it in Jupyter notebook.
    
    Args:
        model_class: A Pydantic model class (subclass of BaseModel)
    """
    if not issubclass(model_class, BaseModel):
        raise TypeError("Input must be a Pydantic BaseModel class")
    
    md_name = f"## {model_class.__name__}\n"
    md_docstring = f"{inspect.getdoc(model_class)}\n" or ""
    
    # Get source code lines to extract comments
    try:
        source_lines = inspect.getsource(model_class).splitlines()
    except (OSError, TypeError):
        source_lines = []
    
    # Extract property comments from source code
    property_comments = {}
    for i, line in enumerate(source_lines):
        if ":" in line and "#" in line:
            # Extract property name and comment
            property_part = line.split(":")[0].strip()
            comment_part = line.split("#")[1].strip()
            property_comments[property_part] = comment_part
    
    # Start building the markdown table
    table = "\n| Variable | Type | Default | Details |\n"
    table += "|---|---|---|---|\n"
    
    # Get type hints and model fields
    type_hints = get_type_hints(model_class)
    
    # Handle both Pydantic v1 and v2
    model_fields = getattr(model_class, "model_fields", None)
    if model_fields is None:
        model_fields = getattr(model_class, "__fields__", {})
    
    # Process each field
    for field_name, field_type in type_hints.items():
        # Skip private fields and methods
        if field_name.startswith('_'):
            continue
        
        # Get field info
        field_info = None
        if model_fields and field_name in model_fields:
            field_info = model_fields[field_name]
        
        # Format type string
        type_str = _format_type(field_type)
        
        # Get default value
        default_value = "..."  # Pydantic's notation for required fields
        
        # Try to get default from field info
        if field_info:
            # For Pydantic v2
            if hasattr(field_info, "default") and field_info.default is not inspect.Signature.empty:
                default_value = _escape_table_cell(repr(field_info.default))
            # For Pydantic v1
            elif hasattr(field_info, "default") and not field_info.required:
                default_value = _escape_table_cell(repr(field_info.default))
        
        # Get description
        description = ""
        
        # Try to get description from Field
        if field_info and hasattr(field_info, "description") and field_info.description:
            description = _escape_table_cell(field_info.description)
        # Fallback to comment
        elif field_name in property_comments:
            description = _escape_table_cell(property_comments[field_name])
        
        # For nested Pydantic models, add a reference note
        if issubclass(field_type, BaseModel) if isinstance(field_type, type) else False:
            description += f" (see `{field_type.__name__}` table)"
        
        # Add row to table
        table += f"| `{field_name}` | `{type_str}` | {default_value} | {description} |\n"
    
    return display(Markdown(md_name + md_docstring + table))
    # return table

# %% ../../nbs/97_gradiochat_utils.ipynb 5
def _format_type(type_hint: Any) -> str:
    """Format a type hint into a readable string."""
    if get_origin(type_hint) is not None:
        # Handle generic types like List[str], Optional[int], etc.
        origin = get_origin(type_hint)
        args = get_args(type_hint)
        
        if origin is Union:
            # Handle Optional (Union[X, None])
            if len(args) == 2 and args[1] is type(None):
                return f"Optional[{_format_type(args[0])}]"
            else:
                return f"Union[{', '.join(_format_type(arg) for arg in args)}]"
        
        # Handle other generic types
        origin_name = origin.__name__ if hasattr(origin, "__name__") else str(origin).replace("typing.", "")
        args_str = ", ".join(_format_type(arg) for arg in args)
        return f"{origin_name}[{args_str}]"
    
    # Handle non-generic types
    if hasattr(type_hint, "__name__"):
        return type_hint.__name__
    
    return str(type_hint).replace("typing.", "")

# %% ../../nbs/97_gradiochat_utils.ipynb 6
def _escape_table_cell(text: str) -> str:
    """
    Escape special characters in markdown table cells.
    The key is to escape pipe characters with HTML entity or backslash.
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Replace pipe characters with HTML entity
    # This is the most reliable way to prevent them from being interpreted as column separators
    return text.replace("|", "\|")
