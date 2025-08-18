# api_clients/model_api.py
from .base_api import BaseAPIClient
from typing import Dict, Any, List, Union, Optional
import base64
import os
import mimetypes
import logging

class ModelAPI(BaseAPIClient):
    """
    Flexible API client for both text and multimodal models.
    Supports various message formats and model types.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        super().__init__(base_url, api_key, timeout)
        self.logger = logging.getLogger(__name__)
    
    def send_text_message(
        self, 
        model: str, 
        prompt: str, 
        system_message: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a text-only message to the model.
        
        Args:
            model: Model identifier
            prompt: User prompt
            system_message: Optional system message
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "messages": messages,
            "model": model,
            **kwargs
        }
        
        self.logger.info(f"Sending text message to {model}")
        response = self.post("chat/completions", data=payload)
        return response.json()
    
    def send_multimodal_message(
        self, 
        model: str, 
        prompt: str, 
        images: List[str], 
        system_message: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a multimodal message with text and images.
        
        Args:
            model: Model identifier
            prompt: Text prompt
            images: List of image paths or base64 strings
            system_message: Optional system message
            **kwargs: Additional parameters
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # Build multimodal content
        content = []
        
        # Add text
        if prompt:
            content.append({"type": "text", "text": prompt})
        
        # Add images
        for image in images:
            if os.path.isfile(image):
                # Handle file path
                image_content = self._encode_image_file(image)
            elif image.startswith('data:image') or image.startswith('/9j/'):
                # Handle base64 string
                image_content = {"type": "image_url", "image_url": {"url": image}}
            else:
                # Assume it's a URL
                image_content = {"type": "image_url", "image_url": {"url": image}}
            
            content.append(image_content)
        
        messages.append({"role": "user", "content": content})
        
        payload = {
            "messages": messages,
            "model": model,
            **kwargs
        }
        
        self.logger.info(f"Sending multimodal message to {model} with {len(images)} images")
        response = self.post("chat/completions", data=payload)
        return response.json()
    
    def send_conversation(
        self, 
        model: str, 
        messages: List[Dict[str, Any]], 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a conversation with multiple messages.
        
        Args:
            model: Model identifier
            messages: List of message objects
            **kwargs: Additional parameters
        """
        payload = {
            "messages": messages,
            "model": model,
            **kwargs
        }
        
        self.logger.info(f"Sending conversation to {model} with {len(messages)} messages")
        response = self.post("chat/completions", data=payload)
        return response.json()
    
    def generate_embeddings(
        self, 
        model: str, 
        texts: Union[str, List[str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate embeddings for text(s).
        
        Args:
            model: Embedding model identifier
            texts: Single text or list of texts
            **kwargs: Additional parameters
        """
        if isinstance(texts, str):
            texts = [texts]
        
        payload = {
            "model": model,
            "input": texts,
            **kwargs
        }
        
        self.logger.info(f"Generating embeddings with {model} for {len(texts)} texts")
        response = self.post("embeddings", data=payload)
        return response.json()
    
    def _encode_image_file(self, image_path: str) -> Dict[str, Any]:
        """
        Encode an image file to base64 for API requests.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with image content for API
        """
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                
                # Determine MIME type
                mime_type, _ = mimetypes.guess_type(image_path)
                if not mime_type:
                    mime_type = "image/jpeg"  # Default fallback
                
                return {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}"
                    }
                }
        except Exception as e:
            self.logger.error(f"Failed to encode image {image_path}: {e}")
            raise ValueError(f"Could not encode image {image_path}: {e}")
    
    def validate_model_response(self, response: Dict[str, Any]) -> bool:
        """
        Validate the model response structure.
        
        Args:
            response: API response dictionary
            
        Returns:
            True if response is valid
        """
        required_fields = ["choices", "model", "usage"]
        
        for field in required_fields:
            if field not in response:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        if not response["choices"]:
            self.logger.error("Response has no choices")
            return False
        
        choice = response["choices"][0]
        if "message" not in choice:
            self.logger.error("Choice missing message field")
            return False
        
        return True
    
    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model: Model identifier
            
        Returns:
            Model information
        """
        try:
            response = self.get(f"models/{model}")
            return response.json()
        except Exception as e:
            self.logger.warning(f"Could not get model info for {model}: {e}")
            return {}
    
    def list_available_models(self) -> List[Dict[str, Any]]:
        """
        List all available models.
        
        Returns:
            List of available models
        """
        try:
            response = self.get("models")
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            self.logger.warning(f"Could not list models: {e}")
            return []
