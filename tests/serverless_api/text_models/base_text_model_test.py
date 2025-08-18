"""
Base class for text model tests.
Provides common functionality that can be inherited by specific model test classes.
"""

import pytest
import logging
from abc import ABC, abstractmethod

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseTextModelTest(ABC):
    """Base class for all text model tests"""
    
    def __init__(self, model_api):
        self.model_api = model_api
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Model name that should be used for testing"""
        pass
    
    @property
    def model_params(self) -> dict:
        """Default model parameters for testing"""
        return {
            "max_tokens": None,
            "temperature": 1,
            "top_p": 0.9,
            "stream": False
        }
    
    def test_basic_connection(self):
        """Test basic model API connection"""
        self.logger.info(f"Testing {self.model_name} basic connection")
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt="Is this API working correctly?",
            **self.model_params
        )
        
        self._validate_basic_response(response)
        self.logger.info(f"✅ {self.model_name} basic connection test passed")
    
    def test_simple_prompt(self):
        """Test with simple prompt"""
        self.logger.info(f"Testing {self.model_name} with simple prompt")
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt="Hello, how are you?",
            **self.model_params
        )
        
        self._validate_basic_response(response)
        
        # Check content
        content = response["choices"][0]["message"]["content"]
        assert len(content) > 0, "Response content should not be empty"
        
        self.logger.info(f"✅ {self.model_name} simple prompt test passed")
    
    def test_long_prompt(self, prompt_length: int = 5000):
        """Test with long prompt"""
        self.logger.info(f"Testing {self.model_name} with long prompt ({prompt_length} chars)")
        
        long_prompt = "A" * prompt_length
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt=long_prompt,
            **self.model_params
        )
        
        self._validate_basic_response(response)
        self.logger.info(f"✅ {self.model_name} long prompt test passed")
    
    def test_special_characters(self):
        """Test with special characters and emojis"""
        self.logger.info(f"Testing {self.model_name} with special characters")
        
        special_prompt = "What is 2+2? 😊 Test special chars: @#$%^&*()"
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt=special_prompt,
            **self.model_params
        )
        
        self._validate_basic_response(response)
        self.logger.info(f"✅ {self.model_name} special characters test passed")
    
    def test_empty_prompt(self):
        """Test with empty prompt (should fail)"""
        self.logger.info(f"Testing {self.model_name} with empty prompt")
        
        try:
            response = self.model_api.send_text_message(
                model=self.model_name,
                prompt="",
                **self.model_params
            )
            
            # If we get here, the API accepted empty prompt (unexpected)
            self.logger.warning(f"⚠️ {self.model_name} accepted empty prompt unexpectedly")
            
        except Exception as e:
            # Expected to fail
            self.logger.info(f"✅ {self.model_name} properly rejected empty prompt: {e}")
    
    def test_response_structure(self):
        """Test that API response has correct structure"""
        self.logger.info(f"Testing {self.model_name} response structure")
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt="Explain something in simple terms",
            **self.model_params
        )
        
        self._validate_response_structure(response)
        self.logger.info(f"✅ {self.model_name} response structure validation passed")
    
    def test_performance(self, max_response_time: float = 10.0):
        """Test that API responds within reasonable time"""
        import time
        
        self.logger.info(f"Testing {self.model_name} performance (max {max_response_time}s)")
        
        start_time = time.time()
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt="What is the capital of France?",
            **self.model_params
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Check response is valid
        self._validate_basic_response(response)
        
        # Check response time
        assert response_time < max_response_time, f"Response time {response_time:.2f}s exceeds {max_response_time}s limit"
        
        self.logger.info(f"✅ {self.model_name} performance test passed: {response_time:.2f}s")
    
    def test_custom_prompt(self, prompt: str, expected_content_check=None):
        """Test with custom prompt and optional content validation"""
        self.logger.info(f"Testing {self.model_name} with custom prompt: {prompt[:50]}...")
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt=prompt,
            **self.model_params
        )
        
        self._validate_basic_response(response)
        
        # Optional content validation
        if expected_content_check:
            content = response["choices"][0]["message"]["content"]
            expected_content_check(content)
        
        self.logger.info(f"✅ {self.model_name} custom prompt test passed")
    
    def _validate_basic_response(self, response):
        """Validate basic API response structure"""
        assert "choices" in response, "Response missing 'choices' field"
        assert isinstance(response["choices"], list), "'choices' is not a list"
        assert len(response["choices"]) > 0, "'choices' is empty"
        assert "message" in response["choices"][0], "Missing 'message' in first choice"
        assert "content" in response["choices"][0]["message"], "Missing 'content' in message"
    
    def _validate_response_structure(self, response):
        """Validate detailed API response structure"""
        # Check required fields
        assert "choices" in response, "Response should contain 'choices' field"
        
        # Check data sub-fields
        choices = response["choices"]
        assert isinstance(choices, list), "'choices' should be a list"
        assert len(choices) > 0, "'choices' should not be empty"
        
        first_choice = choices[0]
        assert "message" in first_choice, "First choice should contain 'message'"
        assert "content" in first_choice["message"], "Message should contain 'content'"
        
        # Check field types
        assert isinstance(first_choice["message"]["content"], str), "Content should be string"
    
    def run_all_basic_tests(self):
        """Run all basic tests for the model"""
        self.logger.info(f"🚀 Running all basic tests for {self.model_name}")
        
        self.test_basic_connection()
        self.test_simple_prompt()
        self.test_long_prompt()
        self.test_special_characters()
        self.test_response_structure()
        self.test_performance()
        
        self.logger.info(f"🎉 All basic tests completed for {self.model_name}")
    
    def teardown_method(self):
        """Cleanup after each test method"""
        self.logger.info(f"🧹 Test cleanup completed for {self.model_name}")


# Factory function to create test classes for specific models
def create_model_test_class(model_name: str, custom_params: dict = None):
    """
    Factory function to create a test class for a specific model.
    
    Args:
        model_name: Name of the model to test
        custom_params: Custom model parameters (optional)
    
    Returns:
        A test class that inherits from BaseTextModelTest
    """
    
    class DynamicModelTest(BaseTextModelTest):
        @property
        def model_name(self) -> str:
            return model_name
        
        @property
        def model_params(self) -> dict:
            base_params = super().model_params
            if custom_params:
                base_params.update(custom_params)
            return base_params
    
    # Set class name
    DynamicModelTest.__name__ = f"Test{model_name.replace('/', '_').replace('-', '_')}"
    DynamicModelTest.__doc__ = f"Test class for {model_name}"
    
    return DynamicModelTest 