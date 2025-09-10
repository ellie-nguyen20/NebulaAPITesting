import pytest
import logging
from api_clients.embedding_api import EmbeddingAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestEmbeddingModels:
    """Test suite for embedding models."""

    def test_uae_large_v1_embedding(self, config, api_key_scope_session):
        """Test UAE-Large-V1 embedding model"""
        
        # Initialize embedding API
        embedding_config = {
            "embedding_url": config["embedding_url"],
            "api_key": api_key_scope_session
        }
        embedding_api = EmbeddingAPI(embedding_config)
        
        # Test data
        test_texts = [
            "Bananas are berries, but strawberries are not, according to botanical classifications.",
            "The Eiffel Tower in Paris was originally intended to be a temporary structure."
        ]
        
        print(f"\nTesting UAE-Large-V1 embedding model...")
        print(f"  Input texts: {len(test_texts)} texts")
        
        # Create embeddings
        response = embedding_api.create_embeddings("uae-large-v1", test_texts)
        
        # Validate response
        assert response.ok, f"Embedding creation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        try:
            data = response.json()
            print(f"  Response data keys: {list(data.keys())}")
        except Exception as e:
            pytest.fail(f"Failed to parse JSON response: {e}")
        
        # Validate response structure
        assert "data" in data, "Response missing 'data' field"
        assert "model" in data, "Response missing 'model' field"
        assert "usage" in data, "Response missing 'usage' field"
        
        # Validate data field
        embeddings_data = data["data"]
        assert isinstance(embeddings_data, list), "Data field should be a list"
        assert len(embeddings_data) == len(test_texts), f"Expected {len(test_texts)} embeddings, got {len(embeddings_data)}"
        
        # Validate each embedding
        for i, embedding_item in enumerate(embeddings_data):
            assert isinstance(embedding_item, dict), f"Embedding {i} should be a dictionary"
            assert "embedding" in embedding_item, f"Embedding {i} missing 'embedding' field"
            assert "index" in embedding_item, f"Embedding {i} missing 'index' field"
            
            embedding_vector = embedding_item["embedding"]
            assert isinstance(embedding_vector, list), f"Embedding {i} should be a list"
            assert len(embedding_vector) > 0, f"Embedding {i} should not be empty"
            
            # Check if all values are numbers
            for j, value in enumerate(embedding_vector):
                assert isinstance(value, (int, float)), f"Embedding {i} value {j} should be a number"
        
        # Validate model field
        assert data["model"] == "WhereIsAI/UAE-Large-V1", f"Expected model 'WhereIsAI/UAE-Large-V1', got '{data['model']}'"
        
        # Validate usage field
        usage = data["usage"]
        assert isinstance(usage, dict), "Usage should be a dictionary"
        assert "prompt_tokens" in usage, "Usage missing 'prompt_tokens' field"
        assert "total_tokens" in usage, "Usage missing 'total_tokens' field"
        
        print(f"  Model: {data['model']}")
        print(f"  Embeddings count: {len(embeddings_data)}")
        print(f"  Embedding dimensions: {len(embeddings_data[0]['embedding'])}")
        print(f"  Usage: {usage}")
        print(f"  UAE-Large-V1 embedding test completed successfully!")

    def test_bge_large_en_v1_5_embedding(self, config, api_key_scope_session):
        """Test BGE-Large-EN-V1.5 embedding model"""
        
        # Initialize embedding API
        embedding_config = {
            "embedding_url": config["embedding_url"],
            "api_key": api_key_scope_session
        }
        embedding_api = EmbeddingAPI(embedding_config)
        
        # Test data
        test_texts = [
            "Bananas are berries, but strawberries are not, according to botanical classifications.",
            "The Eiffel Tower in Paris was originally intended to be a temporary structure."
        ]
        
        print(f"\nTesting BGE-Large-EN-V1.5 embedding model...")
        print(f"  Input texts: {len(test_texts)} texts")
        
        # Create embeddings
        response = embedding_api.create_embeddings("bge-large-en-v1.5", test_texts)
        
        # Validate response
        assert response.ok, f"Embedding creation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        try:
            data = response.json()
            print(f"  Response data keys: {list(data.keys())}")
        except Exception as e:
            pytest.fail(f"Failed to parse JSON response: {e}")
        
        # Validate response structure
        assert "data" in data, "Response missing 'data' field"
        assert "model" in data, "Response missing 'model' field"
        assert "usage" in data, "Response missing 'usage' field"
        
        # Validate data field
        embeddings_data = data["data"]
        assert isinstance(embeddings_data, list), "Data field should be a list"
        assert len(embeddings_data) == len(test_texts), f"Expected {len(test_texts)} embeddings, got {len(embeddings_data)}"
        
        # Validate each embedding
        for i, embedding_item in enumerate(embeddings_data):
            assert isinstance(embedding_item, dict), f"Embedding {i} should be a dictionary"
            assert "embedding" in embedding_item, f"Embedding {i} missing 'embedding' field"
            assert "index" in embedding_item, f"Embedding {i} missing 'index' field"
            
            embedding_vector = embedding_item["embedding"]
            assert isinstance(embedding_vector, list), f"Embedding {i} should be a list"
            assert len(embedding_vector) > 0, f"Embedding {i} should not be empty"
            
            # Check if all values are numbers
            for j, value in enumerate(embedding_vector):
                assert isinstance(value, (int, float)), f"Embedding {i} value {j} should be a number"
        
        # Validate model field
        assert data["model"] == "BAAI/bge-large-en-v1.5", f"Expected model 'BAAI/bge-large-en-v1.5', got '{data['model']}'"
        
        # Validate usage field
        usage = data["usage"]
        assert isinstance(usage, dict), "Usage should be a dictionary"
        assert "prompt_tokens" in usage, "Usage missing 'prompt_tokens' field"
        assert "total_tokens" in usage, "Usage missing 'total_tokens' field"
        
        print(f"  Model: {data['model']}")
        print(f"  Embeddings count: {len(embeddings_data)}")
        print(f"  Embedding dimensions: {len(embeddings_data[0]['embedding'])}")
        print(f"  Usage: {usage}")
        print(f"  BGE-Large-EN-V1.5 embedding test completed successfully!")

    def test_qwen3_embedding_8b(self, config, api_key_scope_session):
        """Test Qwen3-Embedding-8B model"""
        
        # Initialize embedding API
        embedding_config = {
            "embedding_url": config["embedding_url"],
            "api_key": api_key_scope_session
        }
        embedding_api = EmbeddingAPI(embedding_config)
        
        # Test data
        test_texts = [
            "Bananas are berries, but strawberries are not, according to botanical classifications.",
            "The Eiffel Tower in Paris was originally intended to be a temporary structure."
        ]
        
        print(f"\nTesting Qwen3-Embedding-8B model...")
        print(f"  Input texts: {len(test_texts)} texts")
        
        # Create embeddings
        response = embedding_api.create_embeddings("qwen3-embedding-8b", test_texts)
        
        # Validate response
        assert response.ok, f"Embedding creation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        try:
            data = response.json()
            print(f"  Response data keys: {list(data.keys())}")
        except Exception as e:
            pytest.fail(f"Failed to parse JSON response: {e}")
        
        # Validate response structure
        assert "data" in data, "Response missing 'data' field"
        assert "model" in data, "Response missing 'model' field"
        assert "usage" in data, "Response missing 'usage' field"
        
        # Validate data field
        embeddings_data = data["data"]
        assert isinstance(embeddings_data, list), "Data field should be a list"
        assert len(embeddings_data) == len(test_texts), f"Expected {len(test_texts)} embeddings, got {len(embeddings_data)}"
        
        # Validate each embedding
        for i, embedding_item in enumerate(embeddings_data):
            assert isinstance(embedding_item, dict), f"Embedding {i} should be a dictionary"
            assert "embedding" in embedding_item, f"Embedding {i} missing 'embedding' field"
            assert "index" in embedding_item, f"Embedding {i} missing 'index' field"
            
            embedding_vector = embedding_item["embedding"]
            assert isinstance(embedding_vector, list), f"Embedding {i} should be a list"
            assert len(embedding_vector) > 0, f"Embedding {i} should not be empty"
            
            # Check if all values are numbers
            for j, value in enumerate(embedding_vector):
                assert isinstance(value, (int, float)), f"Embedding {i} value {j} should be a number"
        
        # Validate model field
        assert data["model"] == "Qwen/Qwen3-Embedding-8B", f"Expected model 'Qwen/Qwen3-Embedding-8B', got '{data['model']}'"
        
        # Validate usage field
        usage = data["usage"]
        assert isinstance(usage, dict), "Usage should be a dictionary"
        assert "prompt_tokens" in usage, "Usage missing 'prompt_tokens' field"
        assert "total_tokens" in usage, "Usage missing 'total_tokens' field"
        
        print(f"  Model: {data['model']}")
        print(f"  Embeddings count: {len(embeddings_data)}")
        print(f"  Embedding dimensions: {len(embeddings_data[0]['embedding'])}")
        print(f"  Usage: {usage}")
        print(f"  Qwen3-Embedding-8B test completed successfully!")

    def test_embedding_dimensions(self, config, api_key_scope_session):
        """Test getting embedding dimensions for different models"""
        
        # Initialize embedding API
        embedding_config = {
            "embedding_url": config["embedding_url"],
            "api_key": api_key_scope_session
        }
        embedding_api = EmbeddingAPI(embedding_config)
        
        models = ["uae-large-v1", "bge-large-en-v1.5", "qwen3-embedding-8b"]
        
        print(f"\nTesting embedding dimensions for different models...")
        
        for model in models:
            print(f"  Testing {model}...")
            
            dimensions = embedding_api.get_embedding_dimensions(model, "test text")
            
            assert dimensions is not None, f"Failed to get dimensions for {model}"
            assert dimensions > 0, f"Dimensions should be positive for {model}"
            
            print(f"    Dimensions: {dimensions}")
        
        print(f"  Embedding dimensions test completed successfully!")

    def test_compare_embeddings(self, config, api_key_scope_session):
        """Test comparing two texts using embeddings"""
        
        # Initialize embedding API
        embedding_config = {
            "embedding_url": config["embedding_url"],
            "api_key": api_key_scope_session
        }
        embedding_api = EmbeddingAPI(embedding_config)
        
        # Test texts
        text1 = "The cat is sleeping on the couch."
        text2 = "A feline is resting on the sofa."
        text3 = "The weather is sunny today."
        
        print(f"\nTesting embedding comparison...")
        print(f"  Text 1: {text1}")
        print(f"  Text 2: {text2}")
        print(f"  Text 3: {text3}")
        
        # Get embeddings for comparison
        response = embedding_api.compare_embeddings("uae-large-v1", text1, text2)
        assert response.ok, f"Embedding comparison failed with status {response.status_code}"
        
        data = response.json()
        embeddings = data["data"]
        
        assert len(embeddings) == 2, f"Expected 2 embeddings, got {len(embeddings)}"
        
        # Get embeddings for text3
        response3 = embedding_api.compare_embeddings("uae-large-v1", text1, text3)
        assert response3.ok, f"Embedding comparison failed with status {response3.status_code}"
        
        data3 = response3.json()
        embeddings3 = data3["data"]
        
        print(f"  Embeddings generated successfully!")
        print(f"  Text1-Text2 embeddings: {len(embeddings[0]['embedding'])} dimensions")
        print(f"  Text1-Text3 embeddings: {len(embeddings3[0]['embedding'])} dimensions")
        
        print(f"  Embedding comparison test completed successfully!")

    def test_batch_embeddings(self, config, api_key_scope_session):
        """Test batch processing of embeddings"""
        
        # Initialize embedding API
        embedding_config = {
            "embedding_url": config["embedding_url"],
            "api_key": api_key_scope_session
        }
        embedding_api = EmbeddingAPI(embedding_config)
        
        # Create a batch of test texts
        test_texts = [
            f"Test text number {i} for batch processing." for i in range(5)
        ]
        
        print(f"\nTesting batch embeddings...")
        print(f"  Batch size: {len(test_texts)} texts")
        
        # Process batch
        responses = embedding_api.batch_embeddings("uae-large-v1", test_texts, batch_size=3)
        
        assert len(responses) > 0, "Should have at least one batch response"
        
        total_embeddings = 0
        for i, response in enumerate(responses):
            assert response.ok, f"Batch {i} failed with status {response.status_code}"
            
            data = response.json()
            embeddings = data["data"]
            total_embeddings += len(embeddings)
            
            print(f"    Batch {i+1}: {len(embeddings)} embeddings")
        
        assert total_embeddings == len(test_texts), f"Expected {len(test_texts)} total embeddings, got {total_embeddings}"
        
        print(f"  Total embeddings processed: {total_embeddings}")
        print(f"  Batch embeddings test completed successfully!")

    def test_embedding_error_handling(self, config, api_key_scope_session):
        """Test error handling for embedding API"""
        
        # Initialize embedding API
        embedding_config = {
            "embedding_url": config["embedding_url"],
            "api_key": api_key_scope_session
        }
        embedding_api = EmbeddingAPI(embedding_config)
        
        print(f"\nTesting embedding error handling...")
        
        # Test with invalid model
        print(f"  Testing invalid model...")
        response = embedding_api.create_embeddings("invalid-model", "test text")
        
        if response.ok:
            print(f"    Invalid model accepted (unexpected)")
        else:
            print(f"    Invalid model correctly rejected: {response.status_code}")
            assert response.status_code in [400, 404, 422], f"Expected 400/404/422 for invalid model, got {response.status_code}"
        
        # Test with empty input
        print(f"  Testing empty input...")
        response = embedding_api.create_embeddings("uae-large-v1", [])
        
        if response.ok:
            print(f"    Empty input accepted (unexpected)")
        else:
            print(f"    Empty input correctly rejected: {response.status_code}")
            assert response.status_code in [400, 422], f"Expected 400/422 for empty input, got {response.status_code}"
        
        print(f"  Error handling test completed successfully!")
