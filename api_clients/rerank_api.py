from .base_model import BaseModel
from typing import Dict, Any, List, Optional, Union
import logging
import requests

class RerankAPI(BaseModel):
    """
    API client for rerank models.
    
    This client provides a simplified interface for calling rerank models
    to rank documents based on their relevance to a query.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize RerankAPI with configuration.
        
        Args:
            config: Configuration dictionary containing:
                - rerank_url: URL for rerank endpoint
                - api_key: API key for authentication
        """
        if 'rerank_url' not in config:
            raise ValueError("rerank_url is required in config. Please check your config.yaml file.")
        
        rerank_url = config['rerank_url']
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Using rerank_url: {rerank_url}")
        
        super().__init__(rerank_url, config['api_key'])
        
        # Predefined model configurations for rerank models
        self.model_configs = {
            "bge-reranker-v2-m3": {
                "model": "BAAI/bge-reranker-v2-m3",
                "top_n": 3
            },
            "bge-reranker-base": {
                "model": "BAAI/bge-reranker-base",
                "top_n": 3
            },
            "bge-reranker-large": {
                "model": "BAAI/bge-reranker-large",
                "top_n": 3
            }
        }
    
    def rerank_documents(self, model: str, query: str, documents: List[str], top_n: int = 3, **kwargs):
        """
        Rerank documents based on their relevance to a query.
        
        Args:
            model: Model name or model config key
            query: Query string to rank documents against
            documents: List of documents to rank
            top_n: Number of top documents to return
            **kwargs: Additional parameters
        
        Returns:
            Response object with reranked documents
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
            "query": query,
            "documents": documents,
            "top_n": top_n
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
        
        self.logger.debug(f"Making rerank request to: {self.base_model_url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Payload: {payload}")
        
        response = requests.post(self.base_model_url, headers=headers, json=payload)
        
        if response.status_code != 200:
            self.logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        return response
    
    def test_rerank_model(self, model: str, query: str = None, documents: List[str] = None):
        """
        Test a rerank model with sample data.
        
        Args:
            model: Model name or model config key to test
            query: Query string (defaults to sample query)
            documents: List of documents (defaults to sample documents)
        
        Returns:
            Response object with reranked documents
        """
        if query is None:
            query = "What is the capital of Canada?"
        
        if documents is None:
            documents = [
                "Ottawa is the capital city of Canada and sits on the Ottawa River near the Ontario-Quebec border.",
                "Montreal is the largest city in Quebec, known for festivals and food, but it is not the national capital.",
                "Toronto is the capital of the province of Ontario, not the country of Canada.",
                "Quebec City is the capital of Quebec; Montreal is the province's largest city."
            ]
        
        return self.rerank_documents(model, query, documents)
    
    def get_rerank_scores(self, model: str, query: str, documents: List[str], top_n: int = 3):
        """
        Get rerank scores for documents.
        
        Args:
            model: Model name or model config key
            query: Query string to rank documents against
            documents: List of documents to rank
            top_n: Number of top documents to return
        
        Returns:
            List of reranked documents with scores
        """
        response = self.rerank_documents(model, query, documents, top_n)
        
        if response.ok:
            data = response.json()
            if "results" in data:
                return data["results"]
        
        return []
    
    def compare_queries(self, model: str, queries: List[str], documents: List[str], top_n: int = 3):
        """
        Compare multiple queries against the same set of documents.
        
        Args:
            model: Model name or model config key
            queries: List of queries to test
            documents: List of documents to rank
            top_n: Number of top documents to return for each query
        
        Returns:
            Dictionary with query results
        """
        results = {}
        
        for i, query in enumerate(queries):
            print(f"  Testing query {i+1}: {query}")
            response = self.rerank_documents(model, query, documents, top_n)
            
            if response.ok:
                data = response.json()
                results[query] = data.get("results", [])
            else:
                results[query] = []
        
        return results
    
    def batch_rerank(self, model: str, query_document_pairs: List[Dict[str, Any]], top_n: int = 3):
        """
        Rerank multiple query-document pairs in batch.
        
        Args:
            model: Model name or model config key
            query_document_pairs: List of dicts with 'query' and 'documents' keys
            top_n: Number of top documents to return for each query
        
        Returns:
            List of response objects for each query
        """
        responses = []
        
        for i, pair in enumerate(query_document_pairs):
            query = pair.get("query", "")
            documents = pair.get("documents", [])
            
            print(f"  Processing batch {i+1}: {query[:50]}...")
            response = self.rerank_documents(model, query, documents, top_n)
            responses.append(response)
        
        return responses
