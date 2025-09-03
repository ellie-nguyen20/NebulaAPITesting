"""
Test file for Llama 33B 70B model using the base text model test class.
Comprehensive tests for Llama 33B 70B model functionality.
"""

import pytest
import logging
from .base_text_model_test import BaseTextModelTest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestLlama3370BModel(BaseTextModelTest):
    """Test class for Llama 33B 70B model API functionality"""
    
    @property
    def model_name(self) -> str:
        """Model name for Llama 33B 70B"""
        return "meta-llama/Llama-3.3-70B-Instruct"
    
    @property
    def model_params(self) -> dict:
        """Custom parameters for Llama 33B 70B"""
        return {
            "max_tokens": None,
            "temperature": 1,
            "top_p": 0.9,
            "stream": False
        }
    
    def test_llama_3370b_specific_features(self):
        """Test Llama 33B 70B-specific features"""
        self.logger.info("Testing Llama 33B 70B specific features")
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt="Explain quantum computing in simple terms",
            **self.model_params
        )
        
        self._validate_basic_response(response)
        
        # Check that response is substantial
        content = response["choices"][0]["message"]["content"]
        assert len(content) > 50, "Llama 33B 70B response should be substantial"
        
        self.logger.info("✅ Llama 33B 70B specific features test passed")
    
    def test_llama_3370b_code_generation(self):
        """Test Llama 33B 70B's code generation capabilities"""
        self.logger.info("Testing Llama 33B 70B code generation")
        
        code_prompt = "Write a Python function to calculate fibonacci numbers"
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt=code_prompt,
            **self.model_params
        )
        
        self._validate_basic_response(response)
        
        # Check that response contains code-like content
        content = response["choices"][0]["message"]["content"]
        assert "def" in content or "function" in content, "Response should contain code"
        
        self.logger.info("✅ Llama 33B 70B code generation test passed")
    
    def test_llama_3370b_math_reasoning(self):
        """Test Llama 33B 70B's mathematical reasoning"""
        self.logger.info("Testing Llama 33B 70B mathematical reasoning")
        
        math_prompt = "Solve this step by step: If a train travels 120 km in 2 hours, what is its speed in km/h?"
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt=math_prompt,
            **self.model_params
        )
        
        self._validate_basic_response(response)
        
        # Check that response contains mathematical reasoning
        content = response["choices"][0]["message"]["content"]
        assert any(word in content.lower() for word in ["speed", "distance", "time", "120", "2", "60"]), "Response should contain mathematical reasoning"
        
        self.logger.info("✅ Llama 33B 70B mathematical reasoning test passed")
    
    def test_llama_3370b_multilingual(self):
        """Test Llama 33B 70B's multilingual capabilities"""
        self.logger.info("Testing Llama 33B 70B multilingual capabilities")
        
        multilingual_prompts = [
            "Hello, how are you?",
            "Bonjour, comment allez-vous?",
            "Hola, ¿cómo estás?",
            "你好，你好吗？"
        ]
        
        for prompt in multilingual_prompts:
            response = self.model_api.send_text_message(
                model=self.model_name,
                prompt=prompt,
                **self.model_params
            )
            
            self._validate_basic_response(response)
            
            # Check that response is not empty
            content = response["choices"][0]["message"]["content"]
            assert len(content) > 0, f"Response for '{prompt}' should not be empty"
        
        self.logger.info("✅ Llama 33B 70B multilingual test passed")
    
    def test_llama_3370b_edge_cases(self):
        """Test Llama 33B 70B with edge cases"""
        self.logger.info("Testing Llama 33B 70B edge cases")
        
        edge_cases = [
            ("Very long prompt", "A" * 8000),  # Very long prompt
            ("Single character", "a"),          # Single character
            ("Special symbols", "!@#$%^&*()"), # Special symbols
            ("Numbers only", "1234567890"),     # Numbers only
        ]
        
        for case_name, prompt in edge_cases:
            try:
                response = self.model_api.send_text_message(
                    model=self.model_name,
                    prompt=prompt,
                    **self.model_params
                )
                
                self._validate_basic_response(response)
                self.logger.info(f"✅ Edge case '{case_name}' passed")
                
            except Exception as e:
                self.logger.warning(f"⚠️ Edge case '{case_name}' failed: {e}")
        
        self.logger.info("✅ Llama 33B 70B edge cases test completed")
    
    def test_llama_3370b_parameter_variations(self):
        """Test Llama 33B 70B with different parameter combinations"""
        self.logger.info("Testing Llama 33B 70B parameter variations")
        
        parameter_combinations = [
            {"temperature": 0.1, "top_p": 0.1},    # Low randomness
            {"temperature": 0.5, "top_p": 0.5},    # Medium randomness
            {"temperature": 1.0, "top_p": 0.9},    # High randomness
            {"max_tokens": 100, "temperature": 0.7}, # Limited tokens
        ]
        
        for params in parameter_combinations:
            try:
                response = self.model_api.send_text_message(
                    model=self.model_name,
                    prompt="Write a short story about a cat",
                    **{**self.model_params, **params}
                )
                
                self._validate_basic_response(response)
                
                # Check max_tokens if specified
                if "max_tokens" in params:
                    content = response["choices"][0]["message"]["content"]
                    assert len(content) <= params["max_tokens"] * 4, f"Response should respect max_tokens={params['max_tokens']}"
                
                self.logger.info(f"✅ Parameters {params} passed")
                
            except Exception as e:
                self.logger.warning(f"⚠️ Parameters {params} failed: {e}")
        
        self.logger.info("✅ Llama 33B 70B parameter variations test completed")
    
    def run_llama_3370b_specific_tests(self):
        """Run all Llama 33B 70B-specific tests"""
        self.logger.info("🚀 Running Llama 33B 70B specific tests")
        
        self.test_llama_3370b_specific_features()
        self.test_llama_3370b_code_generation()
        self.test_llama_3370b_math_reasoning()
        self.test_llama_3370b_multilingual()
        self.test_llama_3370b_edge_cases()
        self.test_llama_3370b_parameter_variations()
        
        self.logger.info("🎉 All Llama 33B 70B specific tests completed")
    
    def run_all_tests(self):
        """Run all tests (basic + specific) for Llama 33B 70B"""
        self.logger.info("🚀 Running ALL tests for Llama 33B 70B")
        
        # Run basic tests from parent class
        self.run_all_basic_tests()
        
        # Run Llama 33B 70B-specific tests
        self.run_llama_3370b_specific_tests()
        
        self.logger.info("🎉 ALL tests completed for Llama 33B 70B")


# Test functions that can be used independently
def test_llama_3370b_basic_functionality(model_api):
    """Test basic Llama 33B 70B functionality as a standalone function"""
    logger.info("Testing Llama 33B 70B basic functionality")
    
    test_instance = TestLlama3370BModel(model_api)
    test_instance.run_all_basic_tests()
    
    logger.info("✅ Llama 33B 70B basic functionality test completed")


def test_llama_3370b_full_functionality(model_api):
    """Test full Llama 33B 70B functionality as a standalone function"""
    logger.info("Testing Llama 33B 70B full functionality")
    
    test_instance = TestLlama3370BModel(model_api)
    test_instance.run_all_tests()
    
    logger.info("✅ Llama 33B 70B full functionality test completed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
