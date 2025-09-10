import pytest
import logging
from api_clients.rerank_api import RerankAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_bge_reranker_v2_m3_basic(config, api_key_scope_session):
    """Test BGE-Reranker-V2-M3 model - Basic functionality"""
    
    # Initialize rerank API
    rerank_config = {
        "rerank_url": config["rerank_url"],
        "api_key": api_key_scope_session
    }
    rerank_api = RerankAPI(rerank_config)
    
    # Test data
    query = "What is the capital of Canada?"
    documents = [
        "Ottawa is the capital city of Canada and sits on the Ottawa River near the Ontario-Quebec border.",
        "Montreal is the largest city in Quebec, known for festivals and food, but it is not the national capital.",
        "Toronto is the capital of the province of Ontario, not the country of Canada.",
        "Quebec City is the capital of Quebec; Montreal is the province's largest city."
    ]
    
    print(f"\nTesting BGE-Reranker-V2-M3 model...")
    print(f"  Query: {query}")
    print(f"  Documents: {len(documents)} documents")
    
    # Rerank documents
    response = rerank_api.rerank_documents("bge-reranker-v2-m3", query, documents, top_n=3)
    
    # Validate response
    assert response.ok, f"Rerank failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f"  Response data keys: {list(data.keys())}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "results" in data, "Response missing 'results' field"
    assert "id" in data, "Response missing 'id' field"
    
    # Validate results field
    results = data["results"]
    assert isinstance(results, list), "Results should be a list"
    assert len(results) <= 3, f"Expected at most 3 results, got {len(results)}"
    
    # Validate each result
    for i, result in enumerate(results):
        assert isinstance(result, dict), f"Result {i} should be a dictionary"
        assert "index" in result, f"Result {i} missing 'index' field"
        assert "relevance_score" in result, f"Result {i} missing 'relevance_score' field"
        assert "document" in result, f"Result {i} missing 'document' field"
        
        # Check if index is valid
        assert 0 <= result["index"] < len(documents), f"Result {i} has invalid index {result['index']}"
        
        # Check if relevance score is a number
        assert isinstance(result["relevance_score"], (int, float)), f"Result {i} relevance_score should be a number"
        
        # Check document structure
        document = result["document"]
        assert isinstance(document, dict), f"Result {i} document should be a dictionary"
        assert "text" in document, f"Result {i} document missing 'text' field"
    
    print(f"  Request ID: {data['id']}")
    print(f"  Results count: {len(results)}")
    print(f"  Top result index: {results[0]['index'] if results else 'None'}")
    print(f"  Top result score: {results[0]['relevance_score'] if results else 'None'}")
    print(f"  BGE-Reranker-V2-M3 test completed successfully!")

def test_bge_reranker_v2_m3_single_document(config, api_key_scope_session):
    """Test BGE-Reranker-V2-M3 with single document"""
    
    # Initialize rerank API
    rerank_config = {
        "rerank_url": config["rerank_url"],
        "api_key": api_key_scope_session
    }
    rerank_api = RerankAPI(rerank_config)
    
    # Single document
    query = "What is the capital of Canada?"
    documents = ["Ottawa is the capital city of Canada."]
    
    print(f"\nTesting BGE-Reranker-V2-M3 with single document...")
    print(f"  Query: {query}")
    print(f"  Document: {documents[0]}")
    
    # Rerank document
    response = rerank_api.rerank_documents("bge-reranker-v2-m3", query, documents, top_n=1)
    
    # Validate response
    assert response.ok, f"Single document rerank failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse and validate
    data = response.json()
    results = data["results"]
    
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"
    assert results[0]["index"] == 0, f"Expected index 0, got {results[0]['index']}"
    assert results[0]["relevance_score"] > 0, "Relevance score should be positive"
    assert "document" in results[0], "Result missing 'document' field"
    assert "text" in results[0]["document"], "Document missing 'text' field"
    
    print(f"  Single document rerank successful!")
    print(f"  Score: {results[0]['relevance_score']}")

def test_bge_reranker_v2_m3_performance(config, api_key_scope_session):
    """Test BGE-Reranker-V2-M3 performance with multiple queries"""
    
    # Initialize rerank API
    rerank_config = {
        "rerank_url": config["rerank_url"],
        "api_key": api_key_scope_session
    }
    rerank_api = RerankAPI(rerank_config)
    
    # Test data
    queries = [
        "What is the capital of Canada?",
        "Which city is the largest in Quebec?",
        "What is the capital of Ontario?"
    ]
    documents = [
        "Ottawa is the capital city of Canada and sits on the Ottawa River near the Ontario-Quebec border.",
        "Montreal is the largest city in Quebec, known for festivals and food, but it is not the national capital.",
        "Toronto is the capital of the province of Ontario, not the country of Canada.",
        "Quebec City is the capital of Quebec; Montreal is the province's largest city."
    ]
    
    print(f"\nTesting BGE-Reranker-V2-M3 performance...")
    print(f"  Queries count: {len(queries)}")
    print(f"  Documents count: {len(documents)}")
    
    start_time = time.time()
    
    # Test each query
    for i, query in enumerate(queries):
        print(f"    Query {i+1}: {query}")
        response = rerank_api.rerank_documents("bge-reranker-v2-m3", query, documents, top_n=2)
        assert response.ok, f"Query {i+1} failed with status {response.status_code}"
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"  Processing time: {duration:.2f} seconds")
    print(f"  Queries per second: {len(queries) / duration:.2f}")
    print(f"  Performance test completed successfully!")

def test_bge_reranker_v2_m3_similarity_ranking(config, api_key_scope_session):
    """Test BGE-Reranker-V2-M3 for similarity-based ranking"""
    
    # Initialize rerank API
    rerank_config = {
        "rerank_url": config["rerank_url"],
        "api_key": api_key_scope_session
    }
    rerank_api = RerankAPI(rerank_config)
    
    # Test data with clear relevance hierarchy
    query = "What is the capital of Canada?"
    documents = [
        "Ottawa is the capital city of Canada and sits on the Ottawa River near the Ontario-Quebec border.",
        "Montreal is the largest city in Quebec, known for festivals and food, but it is not the national capital.",
        "Toronto is the capital of the province of Ontario, not the country of Canada.",
        "Quebec City is the capital of Quebec; Montreal is the province's largest city.",
        "Vancouver is a major city in British Columbia, known for its natural beauty and outdoor activities."
    ]
    
    print(f"\nTesting BGE-Reranker-V2-M3 similarity ranking...")
    print(f"  Query: {query}")
    print(f"  Documents: {len(documents)} documents")
    
    # Rerank documents
    response = rerank_api.rerank_documents("bge-reranker-v2-m3", query, documents, top_n=5)
    
    # Validate response
    assert response.ok, f"Similarity ranking failed with status {response.status_code}"
    
    data = response.json()
    results = data["results"]
    
    assert len(results) > 0, "Should have at least one result"
    
    # Check that results are ranked by relevance score (descending)
    for i in range(len(results) - 1):
        assert results[i]["relevance_score"] >= results[i + 1]["relevance_score"], \
            f"Results should be ranked by relevance score: {results[i]['relevance_score']} < {results[i + 1]['relevance_score']}"
    
    # The first result should be about Ottawa (capital of Canada)
    top_result_index = results[0]["index"]
    top_document = results[0]["document"]["text"]
    
    print(f"  Top result: Document {top_result_index}")
    print(f"  Top document: {top_document[:50]}...")
    print(f"  Top score: {results[0]['relevance_score']}")
    
    # Check that Ottawa (capital) is ranked higher than other cities
    ottawa_ranked = any("Ottawa" in result["document"]["text"] for result in results)
    assert ottawa_ranked, "Ottawa (capital of Canada) should be ranked in results"
    
    print(f"  Similarity ranking test completed successfully!")

def test_bge_reranker_v2_m3_different_top_n(config, api_key_scope_session):
    """Test BGE-Reranker-V2-M3 with different top_n values"""
    
    # Initialize rerank API
    rerank_config = {
        "rerank_url": config["rerank_url"],
        "api_key": api_key_scope_session
    }
    rerank_api = RerankAPI(rerank_config)
    
    # Test data
    query = "What is the capital of Canada?"
    documents = [
        "Ottawa is the capital city of Canada and sits on the Ottawa River near the Ontario-Quebec border.",
        "Montreal is the largest city in Quebec, known for festivals and food, but it is not the national capital.",
        "Toronto is the capital of the province of Ontario, not the country of Canada.",
        "Quebec City is the capital of Quebec; Montreal is the province's largest city."
    ]
    
    print(f"\nTesting BGE-Reranker-V2-M3 with different top_n values...")
    print(f"  Query: {query}")
    print(f"  Documents: {len(documents)} documents")
    
    # Test different top_n values
    for top_n in [1, 2, 3, 4]:
        print(f"    Testing top_n={top_n}...")
        
        response = rerank_api.rerank_documents("bge-reranker-v2-m3", query, documents, top_n=top_n)
        
        assert response.ok, f"Rerank with top_n={top_n} failed with status {response.status_code}"
        
        data = response.json()
        results = data["results"]
        
        assert len(results) <= top_n, f"Expected at most {top_n} results, got {len(results)}"
        assert len(results) <= len(documents), f"Expected at most {len(documents)} results, got {len(results)}"
        
        print(f"      Results: {len(results)}")
    
    print(f"  Different top_n values test completed successfully!")

def test_bge_reranker_v2_m3_edge_cases(config, api_key_scope_session):
    """Test BGE-Reranker-V2-M3 with edge cases"""
    
    # Initialize rerank API
    rerank_config = {
        "rerank_url": config["rerank_url"],
        "api_key": api_key_scope_session
    }
    rerank_api = RerankAPI(rerank_config)
    
    print(f"\nTesting BGE-Reranker-V2-M3 edge cases...")
    
    # Test with very short query
    print(f"  Testing short query...")
    response = rerank_api.rerank_documents("bge-reranker-v2-m3", "Canada", ["Ottawa is the capital of Canada."], top_n=1)
    assert response.ok, f"Short query failed with status {response.status_code}"
    
    # Test with very long query
    print(f"  Testing long query...")
    long_query = "What is the capital city of Canada and can you tell me about its history, geography, and importance as the political center of the country?"
    response = rerank_api.rerank_documents("bge-reranker-v2-m3", long_query, ["Ottawa is the capital city of Canada."], top_n=1)
    assert response.ok, f"Long query failed with status {response.status_code}"
    
    # Test with very short document
    print(f"  Testing short document...")
    response = rerank_api.rerank_documents("bge-reranker-v2-m3", "Canada", ["Ottawa"], top_n=1)
    assert response.ok, f"Short document failed with status {response.status_code}"
    
    # Test with very long document
    print(f"  Testing long document...")
    long_document = "Ottawa is the capital city of Canada and sits on the Ottawa River near the Ontario-Quebec border. It is the fourth-largest city in Canada and serves as the political center of the country. The city is known for its beautiful architecture, including the Parliament Buildings, and its rich cultural heritage. Ottawa is also home to many museums, galleries, and festivals that attract visitors from around the world."
    response = rerank_api.rerank_documents("bge-reranker-v2-m3", "Canada", [long_document], top_n=1)
    assert response.ok, f"Long document failed with status {response.status_code}"
    
    print(f"  Edge cases test completed successfully!")
