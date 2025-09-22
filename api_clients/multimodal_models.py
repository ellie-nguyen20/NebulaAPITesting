from .base_model import BaseModel
from typing import Dict, Any, List, Optional, Union
import logging
import requests

class MultimodalModelsAPI(BaseModel):
    """
    Client for multimodal models supporting text + image inputs.
    Supports Claude Sonnet 4 and GPT-4o Mini models.
    Single method 'call_model' handles both text-only and multimodal calls.
    """
    
    def __init__(self, config: Dict[str, Any]):
        # Always use chat_completions_url from config.yaml
        if 'chat_completions_url' not in config:
            raise ValueError("chat_completions_url is required in config. Please check your config.yaml file.")
        
        chat_url = config['chat_completions_url']
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Using chat_completions_url: {chat_url}")
        
        super().__init__(chat_url, config['api_key'])
        
        # Predefined model configurations
        self.model_configs = {
            "gpt-4o-mini": {
                "model": "openai/gpt-4o-mini",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "gemini-2.5-pro": {
                "model": "gemini/gemini-2.5-pro",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "gemini-2.5-flash": {
                "model": "gemini/gemini-2.5-flash",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "gemini-2.5-flash-lite": {
                "model": "gemini/gemini-2.5-flash-lite",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "gemini-2.0-flash": {
                "model": "gemini/gemini-2.0-flash",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "gemini-2.0-flash-lite": {
                "model": "gemini/gemini-2.0-flash-lite",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            }
        }
    
    def call_model(
        self, 
        model_name: str, 
        prompt: str, 
        images: Optional[List[str]] = None,
        system_message: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call multimodal model with text and optional images.
        
        Args:
            model_name: Model identifier (e.g., 'claude-sonnet-4', 'gpt-4o-mini')
            prompt: Text prompt
            images: Optional list of image paths, URLs, or base64 strings
            system_message: Optional system message
            **kwargs: Override default model parameters
            
        Returns:
            API response dictionary
        """
        # Get model configuration
        model_config = self._get_model_config(model_name)
        if not model_config:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Build messages
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # Build user content
        if images:
            # Multimodal content (text + images)
            content = []
            if prompt:
                content.append({"type": "text", "text": prompt})
            
            for image in images:
                image_content = self._process_image_input(image)
                content.append(image_content)
            
            messages.append({"role": "user", "content": content})
            self.logger.info(f"Calling {model_name} with text prompt and {len(images)} images")
        else:
            # Text-only content
            messages.append({"role": "user", "content": prompt})
            self.logger.info(f"Calling {model_name} with text prompt")
        
        # Merge default config with overrides
        payload = {**model_config, "messages": messages, **kwargs}
        
        # Make direct request since we have full URL
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.logger.debug(f"Making request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")
        
        response = requests.post(self.base_model_url, headers=headers, json=payload)
        
        # Log response for debugging
        self.logger.debug(f"Response status: {response.status_code}")
        self.logger.debug(f"Response headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        return response.json()
    
    def _get_model_config(self, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific model.
        
        Args:
            model_name: Model identifier
            
        Returns:
            Model configuration dictionary or None if not found
        """
        # Support both short names and full model IDs
        if model_name in self.model_configs:
            return self.model_configs[model_name].copy()
        
        # Check if it's a full model ID
        for short_name, config in self.model_configs.items():
            if config["model"] == model_name:
                return config.copy()
        
        return None
    
    def _process_image_input(self, image: str) -> Dict[str, Any]:
        """
        Process image input (file path, URL, or base64).
        
        Args:
            image: Image path, URL, or base64 string
            
        Returns:
            Processed image content for API
        """
        import os
        import base64
        import mimetypes
        
        # If it's a file path
        if os.path.isfile(image):
            try:
                with open(image, "rb") as image_file:
                    image_data = image_file.read()
                    base64_image = base64.b64encode(image_data).decode('utf-8')
                    
                    # Determine MIME type
                    mime_type, _ = mimetypes.guess_type(image)
                    if not mime_type:
                        mime_type = "image/jpeg"  # Default fallback
                    
                    return {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
            except Exception as e:
                self.logger.error(f"Failed to process image file {image}: {e}")
                raise ValueError(f"Could not process image file {image}: {e}")
        
        # If it's already a base64 string
        elif image.startswith('data:image') or image.startswith('/9j/'):
            return {
                "type": "image_url",
                "image_url": {"url": image}
            }
        
        # If it's a URL
        elif image.startswith('http'):
            return {
                "type": "image_url",
                "image_url": {"url": image}
            }
        
        else:
            raise ValueError(f"Invalid image input: {image}. Must be file path, URL, or base64 string")
    
