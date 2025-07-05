"""
AI Model integrations for dataset generation.
Handles Gemini, Claude, and OpenAI models.
"""

import google.generativeai as genai
from typing import Dict, List

# Optional imports with error handling
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ModelManager:
    """Manages AI model integrations and configurations."""
    
    @staticmethod
    def get_available_models() -> List[str]:
        """Get list of available AI model providers."""
        available_models = ["Gemini"]
        if ANTHROPIC_AVAILABLE:
            available_models.append("Claude")
        if OPENAI_AVAILABLE:
            available_models.append("OpenAI")
        return available_models
    
    @staticmethod
    def get_model_variants(provider: str) -> List[str]:
        """Get available model variants for a provider."""
        if provider == "Gemini":
            return ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"]
        elif provider == "Claude":
            return ["claude-sonnet-4-20250514", "claude-3-5-haiku-20241022", "claude-3-7-sonnet-latest"]
        elif provider == "OpenAI":
            return ["gpt-4o", "gpt-4o-mini", "o3-mini"]
        else:
            return []
    
    @staticmethod
    def initialize_model(provider: str, specific_model: str, api_key: str):
        """Initialize a model instance."""
        if provider == "Gemini":
            genai.configure(api_key=api_key)
            return genai.GenerativeModel(specific_model)
        elif provider == "Claude" and ANTHROPIC_AVAILABLE:
            return anthropic.Anthropic(api_key=api_key)
        elif provider == "OpenAI" and OPENAI_AVAILABLE:
            return openai.OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Unsupported model provider: {provider}")
    
    @staticmethod
    def get_model_response(model, provider: str, specific_model: str, prompt: str) -> str:
        """Get response from the selected AI model."""
        if provider == "Gemini":
            response = model.generate_content(prompt)
            return response.text if response.text else ""
        
        elif provider == "Claude":
            response = model.messages.create(
                model=specific_model,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text if response.content else ""
        
        elif provider == "OpenAI":
            # Handle different parameter requirements for different OpenAI models
            if "o1-" in specific_model or "o3-" in specific_model:
                # o1 and o3 models use max_completion_tokens instead of max_tokens
                response = model.chat.completions.create(
                    model=specific_model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_completion_tokens=4000
                )
            else:
                # Standard GPT models use max_tokens
                response = model.chat.completions.create(
                    model=specific_model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=4000,
                    temperature=0.7
                )
            return response.choices[0].message.content if response.choices else ""
        
        else:
            raise ValueError(f"Unsupported model provider: {provider}") 