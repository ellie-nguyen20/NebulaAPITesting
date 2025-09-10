import pytest
import logging
from api_clients.embedding_api import EmbeddingAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_bge_large_en_v1_5_embedding_basic(config, api_key_scope_session):
    """Test BGE-Large-EN-V1.5 embedding model - Basic functionality"""
    
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

def test_bge_large_en_v1_5_single_text(config, api_key_scope_session):
    """Test BGE-Large-EN-V1.5 with single text input"""
    
    # Initialize embedding API
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    embedding_api = EmbeddingAPI(embedding_config)
    
    # Single text
    test_text = "This is a single text for BGE embedding."
    
    print(f"\nTesting BGE-Large-EN-V1.5 with single text...")
    print(f"  Text: {test_text}")
    
    # Create embedding
    response = embedding_api.create_embeddings("bge-large-en-v1.5", test_text)
    
    # Validate response
    assert response.ok, f"Single text embedding failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse and validate
    data = response.json()
    embeddings_data = data["data"]
    
    assert len(embeddings_data) == 1, f"Expected 1 embedding, got {len(embeddings_data)}"
    assert len(embeddings_data[0]["embedding"]) > 0, "Embedding should not be empty"
    
    print(f"  Single text embedding successful!")
    print(f"  Dimensions: {len(embeddings_data[0]['embedding'])}")

def test_bge_large_en_v1_5_dimensions(config, api_key_scope_session):
    """Test BGE-Large-EN-V1.5 embedding dimensions"""
    
    # Initialize embedding API
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    embedding_api = EmbeddingAPI(embedding_config)
    
    print(f"\nTesting BGE-Large-EN-V1.5 dimensions...")
    
    # Get dimensions
    dimensions = embedding_api.get_embedding_dimensions("bge-large-en-v1.5", "test text")
    
    assert dimensions is not None, "Failed to get dimensions"
    assert dimensions > 0, "Dimensions should be positive"
    
    print(f"  Embedding dimensions: {dimensions}")
    print(f"  Dimensions test completed successfully!")

def test_bge_large_en_v1_5_performance(config, api_key_scope_session):
    """Test BGE-Large-EN-V1.5 performance with multiple texts"""
    
    # Initialize embedding API
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    embedding_api = EmbeddingAPI(embedding_config)
    
    # Create multiple test texts
    test_texts = [
        f"Performance test text number {i} for BGE-Large-EN-V1.5 model." 
        for i in range(10)
    ]
    
    print(f"\nTesting BGE-Large-EN-V1.5 performance...")
    print(f"  Texts count: {len(test_texts)}")
    
    start_time = time.time()
    
    # Create embeddings
    response = embedding_api.create_embeddings("bge-large-en-v1.5", test_texts)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Validate response
    assert response.ok, f"Performance test failed with status {response.status_code}"
    
    data = response.json()
    embeddings_data = data["data"]
    
    assert len(embeddings_data) == len(test_texts), f"Expected {len(test_texts)} embeddings, got {len(embeddings_data)}"
    
    print(f"  Processing time: {duration:.2f} seconds")
    print(f"  Texts per second: {len(test_texts) / duration:.2f}")
    print(f"  Performance test completed successfully!")

def test_bge_large_en_v1_5_similarity(config, api_key_scope_session):
    """Test BGE-Large-EN-V1.5 for text similarity comparison"""
    
    # Initialize embedding API
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    embedding_api = EmbeddingAPI(embedding_config)
    
    # Similar texts
    text1 = "The cat is sleeping on the couch."
    text2 = "A feline is resting on the sofa."
    text3 = "The weather is sunny today."
    
    print(f"\nTesting BGE-Large-EN-V1.5 similarity...")
    print(f"  Text 1: {text1}")
    print(f"  Text 2: {text2}")
    print(f"  Text 3: {text3}")
    
    # Get embeddings for comparison
    response = embedding_api.compare_embeddings("bge-large-en-v1.5", text1, text2)
    assert response.ok, f"Similarity test failed with status {response.status_code}"
    
    data = response.json()
    embeddings = data["data"]
    
    assert len(embeddings) == 2, f"Expected 2 embeddings, got {len(embeddings)}"
    
    # Get embeddings for text3
    response3 = embedding_api.compare_embeddings("bge-large-en-v1.5", text1, text3)
    assert response3.ok, f"Similarity test failed with status {response3.status_code}"
    
    data3 = response3.json()
    embeddings3 = data3["data"]
    
    print(f"  Similarity embeddings generated successfully!")
    print(f"  Text1-Text2 embeddings: {len(embeddings[0]['embedding'])} dimensions")
    print(f"  Text1-Text3 embeddings: {len(embeddings3[0]['embedding'])} dimensions")
    print(f"  Similarity test completed successfully!")
