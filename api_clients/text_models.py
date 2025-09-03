from .base_model import BaseModel
from typing import Dict, Any, List, Optional, Union
import logging
import requests

class TextModelsAPI(BaseModel):
    """
    API client for text-only models.
    
    This client provides a simplified interface for calling text models
    without image support, optimized for text-only conversations.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize TextModelsAPI with configuration.
        
        Args:
            config: Configuration dictionary containing:
                - chat_completions_url: URL for chat completions endpoint
                - api_key: API key for authentication
        """
        if 'chat_completions_url' not in config:
            raise ValueError("chat_completions_url is required in config. Please check your config.yaml file.")
        
        chat_url = config['chat_completions_url']
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Using chat_completions_url: {chat_url}")
        
        super().__init__(chat_url, config['api_key'])
        
        # Predefined model configurations for text models
        self.model_configs = {
            "l3.3-ms-nevoria-70b": {
                "model": "Steelskull/L3.3-MS-Nevoria-70b",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "mistral-small-3.2-24b": {
                "model": "mistralai/Mistral-Small-3.2-24B-Instruct-2506",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "midnight-rose-70b": {
                "model": "sophosympatheia/Midnight-Rose-70B-v2.0.3",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "l3-70b-euryale": {
                "model": "Sao10K/L3-70B-Euryale-v2.1",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "l3-8b-stheno": {
                "model": "Sao10K/L3-8B-Stheno-v3.2",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "deepseek-r1-0528-free": {
                "model": "deepseek-ai/DeepSeek-R1-0528-Free",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "deepseek-r1-0528-paid": {
                "model": "deepseek-ai/DeepSeek-R1-0528",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "deepseek-v3-0324-free": {
                "model": "deepseek-ai/DeepSeek-V3-0324-Free",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "deepseek-v3-0324-paid": {
                "model": "deepseek-ai/DeepSeek-V3-0324",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "deepseek-r1-free": {
                "model": "deepseek-ai/DeepSeek-R1-Free",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "llama-3.3-70b": {
                "model": "meta-llama/Llama-3.3-70B-Instruct",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            },
            "qwq-32b": {
                "model": "Qwen/QwQ-32B",
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
        system_message: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call text model with text prompt only.
        
        Args:
            model_name: Model identifier (e.g., 'gpt-4o-mini', 'claude-sonnet-4')
            prompt: Text prompt
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
        
        # Add user message (text-only)
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
        return self.model_configs.get(model_name)
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available model names.
        
        Returns:
            List of available model identifiers
        """
        return list(self.model_configs.keys())
    
    def chat(
        self, 
        model_name: str, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Chat with a model using a list of messages.
        
        Args:
            model_name: Model identifier
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Override default model parameters
            
        Returns:
            API response dictionary
        """
        # Get model configuration
        model_config = self._get_model_config(model_name)
        if not model_config:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Merge default config with overrides
        payload = {**model_config, "messages": messages, **kwargs}
        
        # Make direct request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.logger.debug(f"Making chat request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")
        
        response = requests.post(self.base_model_url, headers=headers, json=payload)
        
        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        return response.json()
