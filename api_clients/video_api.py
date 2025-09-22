from .base_model import BaseModel
from typing import Dict, Any, List, Optional, Union
import logging
import requests

class VideoAPI(BaseModel):
    """
    API client for video generation models.

    This client provides a simplified interface for calling video generation models
    to create videos from text descriptions or images.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize VideoAPI with configuration.

        Args:
            config: Configuration dictionary containing:
                - video_generation_url: URL for video generation endpoint
                - api_key: API key for authentication
        """
        if 'video_generation_url' not in config:
            raise ValueError("video_generation_url is required in config. Please check your config.yaml file.")

        video_url = config['video_generation_url']
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Using video_generation_url: {video_url}")

        super().__init__(video_url, config['api_key'])

        # Predefined model configurations for video models
        self.model_configs = {
            "seedance-1-0-pro-t2v": {
                "model_name": "Byteplus/seedance-1-0-pro-250528",
                "duration": 5,
                "camera_fixed": False,
                "resolution": "720p",
                "aspect_ratio": "16:9",
                "fps": 1,
                "seed": -1
            },
            "seedance-1-0-pro-i2v": {
                "model_name": "Byteplus/seedance-1-0-pro-250528",
                "duration": 5,
                "camera_fixed": False,
                "resolution": "720p",
                "aspect_ratio": "16:9",
                "fps": 1,
                "seed": -1
            },
            "seedance-1-0-lite-i2v": {
                "model_name": "Byteplus/seedance-1-0-lite-i2v-250428",
                "duration": 5,
                "camera_fixed": False,
                "resolution": "720p",
                "aspect_ratio": "16:9",
                "fps": 1,
                "seed": -1
            },
            "seedance-1-0-lite-t2v": {
                "model_name": "Byteplus/seedance-1-0-lite-t2v-250428",
                "duration": 5,
                "camera_fixed": False,
                "resolution": "720p",
                "aspect_ratio": "16:9",
                "fps": 1,
                "seed": -1
            }
        }

    def generate_video(self, model: str, prompt: str, **kwargs):
        """
        Generate video from text prompt.

        Args:
            model: Model name or model config key
            prompt: Text description for video generation
            **kwargs: Additional parameters (duration, resolution, aspect_ratio, fps, seed, etc.)

        Returns:
            Response object with video generation data
        """
        # Get model configuration if using predefined model
        if model in self.model_configs:
            model_config = self.model_configs[model].copy()
            actual_model = model_config.pop("model_name")
        else:
            actual_model = model
            model_config = {}

        payload = {
            "model_name": actual_model,
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

        self.logger.debug(f"Making video generation request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")

        response = requests.post(self.base_model_url, headers=headers, json=payload)

        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

        return response

    def generate_video_from_image(self, model: str, prompt: str, image_uri: str = "", first_frame_image_uri: str = "", last_frame_image_uri: str = "", **kwargs):
        """
        Generate video from image and text prompt (for i2v models).

        Args:
            model: Model name or model config key (typically i2v models)
            prompt: Text description for video generation
            image_uri: URI of the image (preferred parameter)
            first_frame_image_uri: URI of the first frame image (legacy parameter)
            last_frame_image_uri: URI of the last frame image (legacy parameter)
            **kwargs: Additional parameters

        Returns:
            Response object with video generation data
        """
        # Get model configuration if using predefined model
        if model in self.model_configs:
            model_config = self.model_configs[model].copy()
            actual_model = model_config.pop("model_name")
        else:
            actual_model = model
            model_config = {}

        payload = {
            "model_name": actual_model,
            "prompt": prompt
        }

        # Use image_uri if provided, otherwise fall back to legacy parameters
        if image_uri:
            payload["image_uri"] = image_uri
        else:
            if first_frame_image_uri:
                payload["first_frame_image_uri"] = first_frame_image_uri
            if last_frame_image_uri:
                payload["last_frame_image_uri"] = last_frame_image_uri

        # Add model-specific configuration
        payload.update(model_config)

        # Add any additional parameters
        payload.update(kwargs)

        # Make direct request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        self.logger.debug(f"Making video generation from image request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")

        response = requests.post(self.base_model_url, headers=headers, json=payload)

        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

        return response

    def generate_video_with_resolution(self, model: str, prompt: str, resolution: str = "1080p", **kwargs):
        """
        Generate video with specific resolution.

        Args:
            model: Model name or model config key
            prompt: Text description for video generation
            resolution: Video resolution (e.g., "1080p", "720p")
            **kwargs: Additional parameters

        Returns:
            Response object with video generation data
        """
        return self.generate_video(model, prompt, resolution=resolution, **kwargs)

    def generate_video_with_duration(self, model: str, prompt: str, duration: int = 5, **kwargs):
        """
        Generate video with specific duration.

        Args:
            model: Model name or model config key
            prompt: Text description for video generation
            duration: Video duration in seconds
            **kwargs: Additional parameters

        Returns:
            Response object with video generation data
        """
        return self.generate_video(model, prompt, duration=duration, **kwargs)

    def generate_video_with_aspect_ratio(self, model: str, prompt: str, aspect_ratio: str = "16:9", **kwargs):
        """
        Generate video with specific aspect ratio.

        Args:
            model: Model name or model config key
            prompt: Text description for video generation
            aspect_ratio: Video aspect ratio (e.g., "16:9", "9:16", "1:1")
            **kwargs: Additional parameters

        Returns:
            Response object with video generation data
        """
        return self.generate_video(model, prompt, aspect_ratio=aspect_ratio, **kwargs)
