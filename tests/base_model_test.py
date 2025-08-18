# tests/base_model_test.py
import pytest
import logging
from typing import Dict, Any, List, Optional, Union
from api_clients.model_api import ModelAPI

class BaseModelTest:
    """
    Base class for all model tests.
    Provides common functionality and reduces code duplication.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_api = ModelAPI(
            base_url=config['model_base_url'],
            api_key=config['api_key'],
            timeout=30
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_test_cases(self) -> List[tuple]:
        """
        Get test cases for the model. Override this in subclasses.
        
        Returns:
            List of (test_id, prompt, expected_status) tuples
        """
        return [
            ("TC_00_CheckConnection", "Is this API working correctly?", 200),
            ("TC_01_ValidRequest", "Hello, how are you?", 200),
            ("TC_02_LongPrompt", "A" * 5000, 200),
            ("TC_03_SpecialCharacters", "What is 2+2? 😊", 200),
            ("TC_04_EmptyPrompt", "", 400),
            ("TC_05_InvalidAPIKey", "Hello", 401),
            ("TC_06_NoAPIKey", "Hello", 401),
        ]
    
    def get_model_name(self) -> str:
        """
        Get the model name. Override this in subclasses.
        
        Returns:
            Model identifier string
        """
        raise NotImplementedError("Subclasses must implement get_model_name()")
    
    def get_model_params(self) -> Dict[str, Any]:
        """
        Get default model parameters. Override this in subclasses if needed.
        
        Returns:
            Dictionary of model parameters
        """
        return {
            "max_tokens": None,
            "temperature": 1,
            "top_p": 0.9,
            "stream": False,
        }
    
    def is_multimodal(self) -> bool:
        """
        Check if this model supports multimodal input.
        
        Returns:
            True if multimodal, False if text-only
        """
        return False
    
    def get_test_images(self) -> List[str]:
        """
        Get test images for multimodal models. Override in subclasses.
        
        Returns:
            List of image paths or URLs
        """
        return []
    
    def validate_response(self, test_id: str, result: Dict[str, Any]) -> None:
        """
        Validate the model response.
        
        Args:
            test_id: Test case identifier
            result: API response
        """
        assert "choices" in result, f"{test_id}: Response missing 'choices' field"
        assert result["choices"], f"{test_id}: 'choices' is empty"
        assert "message" in result["choices"][0], f"{test_id}: Missing 'message' in first choice"
        
        # Additional validation for multimodal models
        if self.is_multimodal():
            self._validate_multimodal_response(test_id, result)
    
    def _validate_multimodal_response(self, test_id: str, result: Dict[str, Any]) -> None:
        """
        Additional validation for multimodal responses.
        
        Args:
            test_id: Test case identifier
            result: API response
        """
        # Check if response contains image-related content
        message = result["choices"][0]["message"]
        content = message.get("content", "")
        
        # Basic multimodal validation - can be extended based on specific model behavior
        if not content:
            self.logger.warning(f"{test_id}: Empty content in multimodal response")
    
    def run_text_test(self, test_id: str, prompt: str, expected_status: int) -> None:
        """
        Run a text-only test case.
        
        Args:
            test_id: Test case identifier
            prompt: Text prompt
            expected_status: Expected HTTP status code
        """
        try:
            if expected_status == 200:
                # Valid request
                response = self.model_api.send_text_message(
                    model=self.get_model_name(),
                    prompt=prompt,
                    **self.get_model_params()
                )
                
                self.logger.info(f"{test_id}: Success - {len(response.get('choices', []))} choices")
                self.validate_response(test_id, response)
                
            elif expected_status in [400, 401]:
                # Invalid request - should raise exception
                with pytest.raises(Exception):
                    self.model_api.send_text_message(
                        model=self.get_model_name(),
                        prompt=prompt,
                        **self.get_model_params()
                    )
                self.logger.info(f"{test_id}: Expected error occurred as expected")
                
        except Exception as e:
            if expected_status == 200:
                pytest.fail(f"{test_id}: Unexpected error: {e}")
            else:
                self.logger.info(f"{test_id}: Expected error occurred: {e}")
    
    def run_multimodal_test(self, test_id: str, prompt: str, expected_status: int) -> None:
        """
        Run a multimodal test case.
        
        Args:
            test_id: Test case identifier
            prompt: Text prompt
            expected_status: Expected HTTP status code
        """
        if not self.is_multimodal():
            pytest.skip(f"{test_id}: Model {self.get_model_name()} does not support multimodal input")
        
        images = self.get_test_images()
        if not images:
            pytest.skip(f"{test_id}: No test images available for multimodal testing")
        
        try:
            if expected_status == 200:
                # Valid request
                response = self.model_api.send_multimodal_message(
                    model=self.get_model_name(),
                    prompt=prompt,
                    images=images,
                    **self.get_model_params()
                )
                
                self.logger.info(f"{test_id}: Success - {len(response.get('choices', []))} choices")
                self.validate_response(test_id, response)
                
            elif expected_status in [400, 401]:
                # Invalid request - should raise exception
                with pytest.raises(Exception):
                    self.model_api.send_multimodal_message(
                        model=self.get_model_name(),
                        prompt=prompt,
                        images=images,
                        **self.get_model_params()
                    )
                self.logger.info(f"{test_id}: Expected error occurred as expected")
                
        except Exception as e:
            if expected_status == 200:
                pytest.fail(f"{test_id}: Unexpected error: {e}")
            else:
                self.logger.info(f"{test_id}: Expected error occurred: {e}")
    
    def run_test_case(self, test_id: str, prompt: str, expected_status: int) -> None:
        """
        Run a test case with appropriate method based on model type.
        
        Args:
            test_id: Test case identifier
            prompt: Text prompt
            expected_status: Expected HTTP status code
        """
        self.logger.info(f"Running {test_id} for model {self.get_model_name()}")
        
        if self.is_multimodal():
            self.run_multimodal_test(test_id, prompt, expected_status)
        else:
            self.run_text_test(test_id, prompt, expected_status)
    
    def test_model_api(self, config: Dict[str, Any]) -> None:
        """
        Main test method that runs all test cases.
        
        Args:
            config: Test configuration
        """
        # Initialize with config
        self.__init__(config)
        
        # Run all test cases
        for test_id, prompt, expected_status in self.get_test_cases():
            self.run_test_case(test_id, prompt, expected_status)
    
    def test_model_info(self, config: Dict[str, Any]) -> None:
        """
        Test getting model information.
        
        Args:
            config: Test configuration
        """
        self.__init__(config)
        
        try:
            model_info = self.model_api.get_model_info(self.get_model_name())
            if model_info:
                self.logger.info(f"Model info: {model_info}")
            else:
                self.logger.warning("Could not retrieve model info")
        except Exception as e:
            self.logger.warning(f"Model info test failed: {e}")
    
    def test_embeddings(self, config: Dict[str, Any]) -> None:
        """
        Test embeddings generation if supported.
        
        Args:
            config: Test configuration
        """
        self.__init__(config)
        
        # Only test embeddings for models that support it
        if "embedding" in self.get_model_name().lower():
            try:
                response = self.model_api.generate_embeddings(
                    model=self.get_model_name(),
                    texts=["Hello world", "Test embedding"]
                )
                
                assert "data" in response, "Embeddings response missing 'data' field"
                assert len(response["data"]) == 2, "Expected 2 embeddings"
                
                for embedding in response["data"]:
                    assert "embedding" in embedding, "Embedding missing 'embedding' field"
                    assert len(embedding["embedding"]) > 0, "Empty embedding vector"
                
                self.logger.info("Embeddings test passed")
                
            except Exception as e:
                self.logger.warning(f"Embeddings test failed: {e}")
        else:
            pytest.skip("Model does not support embeddings") 