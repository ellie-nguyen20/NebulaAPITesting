from .base_model import BaseModel
from typing import Dict, Any, List, Optional, Union
import logging
import requests

class VisionAPI(BaseModel):
    """
    API client for vision models.
    
    This client provides a simplified interface for calling vision models
    to process images and text together.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize VisionAPI with configuration.
        
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
        
        # Predefined model configurations for vision models
        self.model_configs = {
            "qwen2.5-vl-7b-instruct": {
                "model": "Qwen/Qwen2.5-VL-7B-Instruct",
                "max_tokens": None,
                "temperature": 1,
                "top_p": 0.9,
                "stream": False
            }
        }
    
    def chat_with_image(self, model: str, image_url: str, text: str, **kwargs):
        """
        Chat with a vision model using an image and text.
        
        Args:
            model: Model name or model config key
            image_url: URL of the image to analyze
            text: Text prompt to send with the image
            **kwargs: Additional parameters
        
        Returns:
            Response object with chat completion
        """
        # Get model configuration if using predefined model
        if model in self.model_configs:
            model_config = self.model_configs[model].copy()
            actual_model = model_config.pop("model")
        else:
            actual_model = model
            model_config = {}
        
        payload = {
            "model": actual_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        },
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        }
        
        # Add model-specific configuration
        payload.update(model_config)
        
        # Add any additional parameters
        payload.update(kwargs)
        
        # Make direct request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.logger.debug(f"Making vision chat request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")
        
        response = requests.post(self.base_model_url, headers=headers, json=payload)
        
        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        return response
    
    def test_vision_model(self, model: str, image_url: str = None, text: str = None):
        """
        Test a vision model with sample data.
        
        Args:
            model: Model name or model config key to test
            image_url: URL of the image to test (defaults to sample image)
            text: Text prompt (defaults to sample prompt)
        
        Returns:
            Response object with chat completion
        """
        if image_url is None:
            image_url = "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"
        
        if text is None:
            text = "What is this image?"
        
        return self.chat_with_image(model, image_url, text)
    
    def analyze_image(self, model: str, image_url: str, analysis_type: str = "general"):
        """
        Analyze an image with different types of analysis.
        
        Args:
            model: Model name or model config key
            image_url: URL of the image to analyze
            analysis_type: Type of analysis (general, objects, text, colors, etc.)
        
        Returns:
            Response object with analysis
        """
        prompts = {
            "general": "What do you see in this image? Describe the main elements and what's happening.",
            "objects": "List all the objects you can identify in this image.",
            "text": "Extract and read any text visible in this image.",
            "colors": "What are the main colors in this image?",
            "emotions": "What emotions or mood does this image convey?",
            "detailed": "Provide a detailed analysis of this image, including objects, people, setting, and any other relevant details."
        }
        
        prompt = prompts.get(analysis_type, prompts["general"])
        return self.chat_with_image(model, image_url, prompt)
    
    def compare_images(self, model: str, image_urls: List[str], text: str = "Compare these images and describe the differences."):
        """
        Compare multiple images.
        
        Args:
            model: Model name or model config key
            image_urls: List of image URLs to compare
            text: Text prompt for comparison
        
        Returns:
            Response object with comparison
        """
        # Get model configuration if using predefined model
        if model in self.model_configs:
            model_config = self.model_configs[model].copy()
            actual_model = model_config.pop("model")
        else:
            actual_model = model
            model_config = {}
        
        # Build content with multiple images
        content = []
        for image_url in image_urls:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            })
        
        content.append({
            "type": "text",
            "text": text
        })
        
        payload = {
            "model": actual_model,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ]
        }
        
        # Add model-specific configuration
        payload.update(model_config)
        
        # Make direct request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.logger.debug(f"Making image comparison request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")
        
        response = requests.post(self.base_model_url, headers=headers, json=payload)
        
        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        return response
    
    def batch_vision_analysis(self, model: str, image_analysis_pairs: List[Dict[str, Any]]):
        """
        Analyze multiple images in batch.
        
        Args:
            model: Model name or model config key
            image_analysis_pairs: List of dicts with 'image_url' and 'text' keys
        
        Returns:
            List of response objects for each analysis
        """
        responses = []
        
        for i, pair in enumerate(image_analysis_pairs):
            image_url = pair.get("image_url", "")
            text = pair.get("text", "What do you see in this image?")
            
            print(f"  Processing batch {i+1}: {text[:50]}...")
            response = self.chat_with_image(model, image_url, text)
            responses.append(response)
        
        return responses
