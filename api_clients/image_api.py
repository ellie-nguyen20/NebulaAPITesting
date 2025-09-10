from .base_model import BaseModel
from typing import Dict, Any, List, Optional, Union
import logging
import requests

class ImageAPI(BaseModel):
    """
    API client for image generation models.

    This client provides a simplified interface for calling image generation models
    to create images from text descriptions.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ImageAPI with configuration.

        Args:
            config: Configuration dictionary containing:
                - image_generation_url: URL for image generation endpoint
                - api_key: API key for authentication
        """
        if 'image_generation_url' not in config:
            raise ValueError("image_generation_url is required in config. Please check your config.yaml file.")

        image_url = config['image_generation_url']
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Using image_generation_url: {image_url}")

        super().__init__(image_url, config['api_key'])

        # Predefined model configurations for image models
        self.model_configs = {
            "bytedance-seedream-3.0": {
                "model": "Bytedance/seedream-3-0-t2i-250415",
                "width": 1024,
                "height": 1024,
                "seed": -1,
                "guidance_scale": 2.5
            },
            "sd-xl-1.0-base": {
                "model": "stabilityai/stable-diffusion-xl-base-1.0",
                "width": 1024,
                "height": 1024,
                "num_steps": 25,
                "guidance_scale": 9,
                "negative_prompt": None
            },
            "flux-1-schnell": {
                "model": "black-forest-labs/FLUX.1-schnell",
                "width": 1024,
                "height": 1024,
                "num_steps": 4,
                "guidance_scale": 3.5,
                "seed": -1
            },
            "flux-1-kontext-dev": {
                "model": "black-forest-labs/FLUX.1-Kontext-dev",
                "width": 1024,
                "height": 1024,
                "guidance_scale": 2.5
            }
        }

    def generate_image(self, model: str, prompt: str, **kwargs):
        """
        Generate image from text prompt.

        Args:
            model: Model name or model config key
            prompt: Text description for image generation
            **kwargs: Additional parameters (width, height, num_images, quality, etc.)

        Returns:
            Response object with image generation data
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
            "prompt": prompt
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

        self.logger.debug(f"Making image generation request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")

        response = requests.post(self.base_model_url, headers=headers, json=payload)

        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

        return response

    def generate_image_with_style(self, model: str, prompt: str, style: str = "realistic", **kwargs):
        """
        Generate image with specific style.

        Args:
            model: Model name or model config key
            prompt: Text description for image generation
            style: Style for image generation (realistic, artistic, cartoon, etc.)
            **kwargs: Additional parameters

        Returns:
            Response object with image generation data
        """
        enhanced_prompt = f"{style} style: {prompt}"
        return self.generate_image(model, enhanced_prompt, **kwargs)

    def generate_multiple_images(self, model: str, prompt: str, num_images: int = 2, **kwargs):
        """
        Generate multiple images from the same prompt.

        Args:
            model: Model name or model config key
            prompt: Text description for image generation
            num_images: Number of images to generate
            **kwargs: Additional parameters

        Returns:
            Response object with multiple image generation data
        """
        return self.generate_image(model, prompt, num_images=num_images, **kwargs)

    def generate_image_with_dimensions(self, model: str, prompt: str, width: int = 1024, height: int = 1024, **kwargs):
        """
        Generate image with specific dimensions.

        Args:
            model: Model name or model config key
            prompt: Text description for image generation
            width: Image width in pixels
            height: Image height in pixels
            **kwargs: Additional parameters

        Returns:
            Response object with image generation data
        """
        return self.generate_image(model, prompt, width=width, height=height, **kwargs)

    def edit_image(self, model: str, prompt: str, image_url: str, **kwargs):
        """
        Edit an existing image using text instructions.

        Args:
            model: Model name or model config key (typically FLUX.1-Kontext-dev)
            prompt: Text instructions for image editing
            image_url: URL of the image to edit
            **kwargs: Additional parameters

        Returns:
            Response object with edited image data
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
            "prompt": prompt,
            "image": image_url
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

        self.logger.debug(f"Making image editing request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")

        response = requests.post(self.base_model_url, headers=headers, json=payload)

        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

        return response
