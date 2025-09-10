from .base_model import BaseModel
from typing import Dict, Any, List, Optional, Union
import logging
import requests

class EmbeddingAPI(BaseModel):
    """
    API client for embedding models.
    
    This client provides a simplified interface for calling embedding models
    to generate vector representations of text.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize EmbeddingAPI with configuration.
        
        Args:
            config: Configuration dictionary containing:
                - embedding_url: URL for embeddings endpoint
                - api_key: API key for authentication
        """
        if 'embedding_url' not in config:
            raise ValueError("embedding_url is required in config. Please check your config.yaml file.")
        
        embedding_url = config['embedding_url']
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Using embedding_url: {embedding_url}")
        
        super().__init__(embedding_url, config['api_key'])
        
        # Predefined model configurations for embedding models
        self.model_configs = {
            "uae-large-v1": {
                "model": "WhereIsAI/UAE-Large-V1",
                "encoding_format": "float",
                "dimensions": None
            },
            "bge-large-en-v1.5": {
                "model": "BAAI/bge-large-en-v1.5",
                "encoding_format": "float",
                "dimensions": None
            },
            "qwen3-embedding-8b": {
                "model": "Qwen/Qwen3-Embedding-8B",
                "encoding_format": "float",
                "dimensions": None
            }
        }
    
    def create_embeddings(self, model: str, input_text: Union[str, List[str]], **kwargs):
        """
        Create embeddings for input text.
        
        Args:
            model: Model name or model config key
            input_text: Text or list of texts to embed
            **kwargs: Additional parameters (encoding_format, dimensions, etc.)
        
        Returns:
            Response object with embeddings data
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
            "input": input_text
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
        
        self.logger.debug(f"Making embedding request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")
        
        response = requests.post(self.base_model_url, headers=headers, json=payload)
        
        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        return response
    
    def test_embedding_model(self, model: str, test_texts: List[str] = None):
        """
        Test an embedding model with sample texts.
        
        Args:
            model: Model name or model config key to test
            test_texts: List of test texts (defaults to sample texts)
        
        Returns:
            Response object with embeddings
        """
        if test_texts is None:
            test_texts = [
                "Bananas are berries, but strawberries are not, according to botanical classifications.",
                "The Eiffel Tower in Paris was originally intended to be a temporary structure."
            ]
        
        return self.create_embeddings(model, test_texts)
    
    def get_embedding_dimensions(self, model: str, sample_text: str = "test"):
        """
        Get the dimensions of embeddings for a specific model.
        
        Args:
            model: Model name or model config key
            sample_text: Sample text to test with
        
        Returns:
            Number of dimensions in the embedding vector
        """
        response = self.create_embeddings(model, sample_text)
        
        if response.ok:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                return len(data["data"][0]["embedding"])
        
        return None
    
    def compare_embeddings(self, model: str, text1: str, text2: str):
        """
        Compare two texts using embeddings and calculate similarity.
        
        Args:
            model: Model name or model config key
            text1: First text to compare
            text2: Second text to compare
        
        Returns:
            Response object with embeddings for both texts
        """
        return self.create_embeddings(model, [text1, text2])
    
    def batch_embeddings(self, model: str, texts: List[str], batch_size: int = 100):
        """
        Create embeddings for a large batch of texts.
        
        Args:
            model: Model name or model config key
            texts: List of texts to embed
            batch_size: Number of texts to process at once
        
        Returns:
            List of response objects for each batch
        """
        responses = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.create_embeddings(model, batch)
            responses.append(response)
        
        return responses
