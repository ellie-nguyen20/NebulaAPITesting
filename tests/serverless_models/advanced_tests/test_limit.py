# """
# Test file for testing API limits and stress testing using the base text model test class.
# Comprehensive tests for API rate limiting, concurrent requests, and performance under load.
# """

# import pytest
# import logging
# import time
# import concurrent.futures
# from .base_text_model_test import BaseTextModelTest

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# class TestAPILimits(BaseTextModelTest):
#     """Test class for API limits and stress testing"""
    
#     @property
#     def model_name(self) -> str:
#         """Model name for limit testing"""
#         return "deepseek-ai/DeepSeek-R1-Free"
    
#     @property
#     def model_params(self) -> dict:
#         """Custom parameters for limit testing"""
#         return {
#             "max_tokens": 100,  # Limit tokens for faster responses
#             "temperature": 0.5,
#             "top_p": 0.9,
#             "stream": False
#         }
    
#     def test_api_20_times_sequential(self):
#         """Test the API 20 times sequentially"""
#         self.logger.info("Testing API 20 times sequentially")
        
#         success_count = 0
#         failure_count = 0
#         total_time = 0
        
#         for i in range(20):
#             start_time = time.time()
            
#             try:
#                 response = self.model_api.send_text_message(
#                     model=self.model_name,
#                     prompt="Is this API working correctly?",
#                     **self.model_params
#                 )
                
#                 end_time = time.time()
#                 request_time = end_time - start_time
#                 total_time += request_time
                
#                 # Validate response
#                 self._validate_basic_response(response)
#                 success_count += 1
                
#                 self.logger.info(f"Loop {i+1}/20: SUCCESS - Time: {request_time:.2f}s")
                
#             except Exception as e:
#                 failure_count += 1
#                 end_time = time.time()
#                 request_time = end_time - start_time
#                 total_time += request_time
                
#                 self.logger.error(f"Loop {i+1}/20: FAILED - {str(e)}, Time: {request_time:.2f}s")
            
#             # Small delay between requests
#             time.sleep(0.5)
        
#         # Summary
#         avg_time = total_time / 20 if total_time > 0 else 0
#         self.logger.info(f"=== Sequential Test Summary ===")
#         self.logger.info(f"Total requests: 20")
#         self.logger.info(f"Successful: {success_count}")
#         self.logger.info(f"Failed: {failure_count}")
#         self.logger.info(f"Success rate: {(success_count/20)*100:.1f}%")
#         self.logger.info(f"Average response time: {avg_time:.2f}s")
#         self.logger.info(f"Total time: {total_time:.2f}s")
        
#         # Assert that at least 80% of requests succeeded
#         assert success_count >= 16, f"Expected at least 16 successful requests, got {success_count}"
    
#     def test_api_concurrent_requests(self, max_workers: int = 5):
#         """Test the API with concurrent requests"""
#         self.logger.info(f"Testing API with {max_workers} concurrent requests")
        
#         def make_request(request_id):
#             """Make a single API request"""
#             try:
#                 start_time = time.time()
                
#                 response = self.model_api.send_text_message(
#                     model=self.model_name,
#                     prompt=f"Test request {request_id}: Is this API working?",
#                     **self.model_params
#                 )
                
#                 end_time = time.time()
#                 request_time = end_time - start_time
                
#                 # Validate response
#                 self._validate_basic_response(response)
                
#                 return {"id": request_id, "success": True, "time": request_time}
                
#             except Exception as e:
#                 end_time = time.time()
#                 request_time = end_time - start_time
                
#                 return {"id": request_id, "success": False, "error": str(e), "time": request_time}
        
#         # Create concurrent requests
#         with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
#             futures = [executor.submit(make_request, i) for i in range(max_workers)]
#             results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
#         # Analyze results
#         success_count = sum(1 for r in results if r["success"])
#         failure_count = len(results) - success_count
        
#         self.logger.info(f"=== Concurrent Test Summary ===")
#         self.logger.info(f"Total concurrent requests: {max_workers}")
#         self.logger.info(f"Successful: {success_count}")
#         self.logger.info(f"Failed: {failure_count}")
#         self.logger.info(f"Success rate: {(success_count/max_workers)*100:.1f}%")
        
#         # Log individual results
#         for result in results:
#             if result["success"]:
#                 self.logger.info(f"Request {result['id']}: SUCCESS - Time: {result['time']:.2f}s")
#             else:
#                 self.logger.error(f"Request {result['id']}: FAILED - {result['error']} - Time: {result['time']:.2f}s")
        
#         # Assert that at least 60% of concurrent requests succeeded
#         assert success_count >= max_workers * 0.6, f"Expected at least {max_workers * 0.6} successful concurrent requests, got {success_count}"
    
#     def test_api_rate_limiting(self):
#         """Test API rate limiting behavior"""
#         self.logger.info("Testing API rate limiting behavior")
        
#         # Make rapid requests to test rate limiting
#         rapid_requests = 10
#         success_count = 0
#         rate_limited_count = 0
        
#         for i in range(rapid_requests):
#             try:
#                 response = self.model_api.send_text_message(
#                     model=self.model_name,
#                     prompt=f"Rapid request {i+1}",
#                     **self.model_params
#                 )
                
#                 self._validate_basic_response(response)
#                 success_count += 1
                
#             except Exception as e:
#                 error_msg = str(e).lower()
#                 if any(phrase in error_msg for phrase in ["rate limit", "too many", "429", "quota"]):
#                     rate_limited_count += 1
#                     self.logger.info(f"Request {i+1}: Rate limited (expected)")
#                 else:
#                     self.logger.error(f"Request {i+1}: Unexpected error - {e}")
            
#             # Very small delay to trigger rate limiting
#             time.sleep(0.1)
        
#         self.logger.info(f"=== Rate Limiting Test Summary ===")
#         self.logger.info(f"Total rapid requests: {rapid_requests}")
#         self.logger.info(f"Successful: {success_count}")
#         self.logger.info(f"Rate limited: {rate_limited_count}")
        
#         # It's okay if some requests are rate limited
#         assert success_count > 0, "Expected at least some requests to succeed"
    
#     def test_api_long_prompt_limits(self):
#         """Test API limits with very long prompts"""
#         self.logger.info("Testing API limits with very long prompts")
        
#         # Test different prompt lengths
#         prompt_lengths = [1000, 5000, 10000, 15000]
        
#         for length in prompt_lengths:
#             try:
#                 long_prompt = "A" * length
                
#                 response = self.model_api.send_text_message(
#                     model=self.model_name,
#                     prompt=long_prompt,
#                     **self.model_params
#                 )
                
#                 self._validate_basic_response(response)
#                 self.logger.info(f"✅ Prompt length {length} chars: SUCCESS")
                
#             except Exception as e:
#                 error_msg = str(e).lower()
#                 if any(phrase in error_msg for phrase in ["too long", "exceeds", "limit", "length"]):
#                     self.logger.info(f"✅ Prompt length {length} chars: Properly rejected (expected)")
#                 else:
#                     self.logger.warning(f"⚠️ Prompt length {length} chars: Unexpected error - {e}")
    
#     def test_api_token_limits(self):
#         """Test API token limits"""
#         self.logger.info("Testing API token limits")
        
#         # Test different max_tokens values
#         token_limits = [10, 50, 100, 200, 500]
        
#         for max_tokens in token_limits:
#             try:
#                 response = self.model_api.send_text_message(
#                     model=self.model_name,
#                     prompt="Write a detailed explanation of artificial intelligence",
#                     **{**self.model_params, "max_tokens": max_tokens}
#                 )
                
#                 self._validate_basic_response(response)
                
#                 # Check that response respects token limit (rough estimate: 1 token ≈ 4 characters)
#                 content = response["choices"][0]["message"]["content"]
#                 estimated_tokens = len(content) / 4
                
#                 if estimated_tokens <= max_tokens * 1.2:  # Allow some tolerance
#                     self.logger.info(f"✅ Max tokens {max_tokens}: SUCCESS (estimated {estimated_tokens:.1f} tokens)")
#                 else:
#                     self.logger.warning(f"⚠️ Max tokens {max_tokens}: Response may exceed limit (estimated {estimated_tokens:.1f} tokens)")
                
#             except Exception as e:
#                 self.logger.warning(f"⚠️ Max tokens {max_tokens}: Failed - {e}")
    
#     def run_all_limit_tests(self):
#         """Run all limit and stress tests"""
#         self.logger.info("🚀 Running all limit and stress tests")
        
#         self.test_api_20_times_sequential()
#         self.test_api_concurrent_requests()
#         self.test_api_rate_limiting()
#         self.test_api_long_prompt_limits()
#         self.test_api_token_limits()
        
#         self.logger.info("🎉 All limit and stress tests completed")
    
#     def run_all_tests(self):
#         """Run all tests (basic + limit)"""
#         self.logger.info("🚀 Running ALL tests for API limits")
        
#         # Run basic tests from parent class
#         self.run_all_basic_tests()
        
#         # Run limit-specific tests
#         self.run_all_limit_tests()
        
#         self.logger.info("🎉 ALL tests completed for API limits")


# # Test functions that can be used independently
# def test_api_limits_basic_functionality(model_api):
#     """Test basic API limits functionality as a standalone function"""
#     logger.info("Testing API limits basic functionality")
    
#     test_instance = TestAPILimits(model_api)
#     test_instance.run_all_basic_tests()
    
#     logger.info("✅ API limits basic functionality test completed")


# def test_api_limits_full_functionality(model_api):
#     """Test full API limits functionality as a standalone function"""
#     logger.info("Testing API limits full functionality")
    
#     test_instance = TestAPILimits(model_api)
#     test_instance.run_all_tests()
    
#     logger.info("✅ API limits full functionality test completed")


# if __name__ == "__main__":
#     pytest.main([__file__, "-v", "-s"])
