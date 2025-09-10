import pytest
import logging
from api_clients.rerank_api import RerankAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestRerankModels:
    """Test suite for rerank models."""

    def test_bge_reranker_v2_m3_basic(self, config, api_key_scope_session):
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

    def test_bge_reranker_v2_m3_single_document(self, config, api_key_scope_session):
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

    def test_bge_reranker_v2_m3_performance(self, config, api_key_scope_session):
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

    def test_rerank_scores(self, config, api_key_scope_session):
        """Test getting rerank scores"""
        
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
        
        print(f"\nTesting rerank scores...")
        print(f"  Query: {query}")
        print(f"  Documents: {len(documents)} documents")
        
        # Get scores
        scores = rerank_api.get_rerank_scores("bge-reranker-v2-m3", query, documents, top_n=3)
        
        assert len(scores) > 0, "Should have at least one score"
        assert len(scores) <= 3, f"Expected at most 3 scores, got {len(scores)}"
        
        # Check that scores are in descending order
        for i in range(len(scores) - 1):
            assert scores[i]["relevance_score"] >= scores[i + 1]["relevance_score"], \
                f"Scores should be in descending order: {scores[i]['relevance_score']} < {scores[i + 1]['relevance_score']}"
        
        print(f"  Scores retrieved successfully!")
        print(f"  Top score: {scores[0]['relevance_score'] if scores else 'None'}")
        print(f"  Scores test completed successfully!")

    def test_compare_queries(self, config, api_key_scope_session):
        """Test comparing multiple queries"""
        
        # Initialize rerank API
        rerank_config = {
            "rerank_url": config["rerank_url"],
            "api_key": api_key_scope_session
        }
        rerank_api = RerankAPI(rerank_config)
        
        # Test data
        queries = [
            "What is the capital of Canada?",
            "Which city is the largest in Quebec?"
        ]
        documents = [
            "Ottawa is the capital city of Canada and sits on the Ottawa River near the Ontario-Quebec border.",
            "Montreal is the largest city in Quebec, known for festivals and food, but it is not the national capital.",
            "Toronto is the capital of the province of Ontario, not the country of Canada.",
            "Quebec City is the capital of Quebec; Montreal is the province's largest city."
        ]
        
        print(f"\nTesting query comparison...")
        print(f"  Queries: {queries}")
        print(f"  Documents: {len(documents)} documents")
        
        # Compare queries
        results = rerank_api.compare_queries("bge-reranker-v2-m3", queries, documents, top_n=2)
        
        assert len(results) == len(queries), f"Expected {len(queries)} query results, got {len(results)}"
        
        for query, result in results.items():
            assert isinstance(result, list), f"Result for query '{query}' should be a list"
            assert len(result) <= 2, f"Expected at most 2 results for query '{query}', got {len(result)}"
        
        print(f"  Query comparison completed successfully!")
        print(f"  Results: {len(results)} queries processed")

    def test_batch_rerank(self, config, api_key_scope_session):
        """Test batch reranking"""
        
        # Initialize rerank API
        rerank_config = {
            "rerank_url": config["rerank_url"],
            "api_key": api_key_scope_session
        }
        rerank_api = RerankAPI(rerank_config)
        
        # Test data
        query_document_pairs = [
            {
                "query": "What is the capital of Canada?",
                "documents": [
                    "Ottawa is the capital city of Canada.",
                    "Montreal is the largest city in Quebec."
                ]
            },
            {
                "query": "Which city is the largest in Quebec?",
                "documents": [
                    "Montreal is the largest city in Quebec.",
                    "Quebec City is the capital of Quebec."
                ]
            }
        ]
        
        print(f"\nTesting batch reranking...")
        print(f"  Query-document pairs: {len(query_document_pairs)}")
        
        # Process batch
        responses = rerank_api.batch_rerank("bge-reranker-v2-m3", query_document_pairs, top_n=2)
        
        assert len(responses) == len(query_document_pairs), f"Expected {len(query_document_pairs)} responses, got {len(responses)}"
        
        for i, response in enumerate(responses):
            assert response.ok, f"Batch {i} failed with status {response.status_code}"
            
            data = response.json()
            results = data.get("results", [])
            print(f"    Batch {i+1}: {len(results)} results")
        
        print(f"  Batch reranking completed successfully!")

    def test_rerank_error_handling(self, config, api_key_scope_session):
        """Test error handling for rerank API"""
        
        # Initialize rerank API
        rerank_config = {
            "rerank_url": config["rerank_url"],
            "api_key": api_key_scope_session
        }
        rerank_api = RerankAPI(rerank_config)
        
        print(f"\nTesting rerank error handling...")
        
        # Test with empty documents
        print(f"  Testing empty documents...")
        response = rerank_api.rerank_documents("bge-reranker-v2-m3", "test query", [], top_n=1)
        
        if response.ok:
            print(f"    Empty documents accepted (unexpected)")
        else:
            print(f"    Empty documents correctly rejected: {response.status_code}")
            assert response.status_code in [400, 422], f"Expected 400/422 for empty documents, got {response.status_code}"
        
        # Test with invalid model
        print(f"  Testing invalid model...")
        response = rerank_api.rerank_documents("invalid-model", "test query", ["test document"], top_n=1)
        
        if response.ok:
            print(f"    Invalid model accepted (unexpected)")
        else:
            print(f"    Invalid model correctly rejected: {response.status_code}")
            assert response.status_code in [400, 404, 422], f"Expected 400/404/422 for invalid model, got {response.status_code}"
        
        print(f"  Error handling test completed successfully!")
