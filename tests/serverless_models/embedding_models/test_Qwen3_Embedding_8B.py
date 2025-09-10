import pytest
import logging
from api_clients.embedding_api import EmbeddingAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_qwen3_embedding_8b_basic(config, api_key_scope_session):
    """Test Qwen3-Embedding-8B model - Basic functionality"""
    
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

def test_qwen3_embedding_8b_single_text(config, api_key_scope_session):
    """Test Qwen3-Embedding-8B with single text input"""
    
    # Initialize embedding API
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    embedding_api = EmbeddingAPI(embedding_config)
    
    # Single text
    test_text = "This is a single text for Qwen3 embedding."
    
    print(f"\nTesting Qwen3-Embedding-8B with single text...")
    print(f"  Text: {test_text}")
    
    # Create embedding
    response = embedding_api.create_embeddings("qwen3-embedding-8b", test_text)
    
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

def test_qwen3_embedding_8b_dimensions(config, api_key_scope_session):
    """Test Qwen3-Embedding-8B embedding dimensions"""
    
    # Initialize embedding API
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    embedding_api = EmbeddingAPI(embedding_config)
    
    print(f"\nTesting Qwen3-Embedding-8B dimensions...")
    
    # Get dimensions
    dimensions = embedding_api.get_embedding_dimensions("qwen3-embedding-8b", "test text")
    
    assert dimensions is not None, "Failed to get dimensions"
    assert dimensions > 0, "Dimensions should be positive"
    
    print(f"  Embedding dimensions: {dimensions}")
    print(f"  Dimensions test completed successfully!")

def test_qwen3_embedding_8b_performance(config, api_key_scope_session):
    """Test Qwen3-Embedding-8B performance with multiple texts"""
    
    # Initialize embedding API
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    embedding_api = EmbeddingAPI(embedding_config)
    
    # Create multiple test texts
    test_texts = [
        f"Performance test text number {i} for Qwen3-Embedding-8B model." 
        for i in range(10)
    ]
    
    print(f"\nTesting Qwen3-Embedding-8B performance...")
    print(f"  Texts count: {len(test_texts)}")
    
    start_time = time.time()
    
    # Create embeddings
    response = embedding_api.create_embeddings("qwen3-embedding-8b", test_texts)
    
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

def test_qwen3_embedding_8b_batch_processing(config, api_key_scope_session):
    """Test Qwen3-Embedding-8B batch processing"""
    
    # Initialize embedding API
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    embedding_api = EmbeddingAPI(embedding_config)
    
    # Create a batch of test texts
    test_texts = [
        f"Batch test text number {i} for Qwen3-Embedding-8B model." 
        for i in range(15)
    ]
    
    print(f"\nTesting Qwen3-Embedding-8B batch processing...")
    print(f"  Batch size: {len(test_texts)} texts")
    
    # Process batch
    responses = embedding_api.batch_embeddings("qwen3-embedding-8b", test_texts, batch_size=5)
    
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
    print(f"  Batch processing test completed successfully!")

def test_qwen3_embedding_8b_multilingual(config, api_key_scope_session):
    """Test Qwen3-Embedding-8B with multilingual text"""
    
    # Initialize embedding API
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    embedding_api = EmbeddingAPI(embedding_config)
    
    # Multilingual test texts
    test_texts = [
        "Hello, how are you today?",  # English
        "Bonjour, comment allez-vous?",  # French
        "Hola, ¿cómo estás?",  # Spanish
        "你好，你今天怎么样？",  # Chinese
        "こんにちは、元気ですか？"  # Japanese
    ]
    
    print(f"\nTesting Qwen3-Embedding-8B multilingual...")
    print(f"  Languages: English, French, Spanish, Chinese, Japanese")
    print(f"  Texts count: {len(test_texts)}")
    
    # Create embeddings
    response = embedding_api.create_embeddings("qwen3-embedding-8b", test_texts)
    
    # Validate response
    assert response.ok, f"Multilingual test failed with status {response.status_code}"
    
    data = response.json()
    embeddings_data = data["data"]
    
    assert len(embeddings_data) == len(test_texts), f"Expected {len(test_texts)} embeddings, got {len(embeddings_data)}"
    
    # Check that all embeddings have the same dimensions
    dimensions = len(embeddings_data[0]["embedding"])
    for i, embedding_item in enumerate(embeddings_data):
        assert len(embedding_item["embedding"]) == dimensions, f"Embedding {i} has different dimensions"
    
    print(f"  Multilingual embeddings generated successfully!")
    print(f"  Embedding dimensions: {dimensions}")
    print(f"  Multilingual test completed successfully!")
