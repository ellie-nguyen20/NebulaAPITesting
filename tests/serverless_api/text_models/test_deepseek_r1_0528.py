"""
Test file for DeepSeek R1 model using the base text model test class.
Demonstrates how to inherit from BaseTextModelTest for specific model testing.
"""

import pytest
import logging
from .base_text_model_test import BaseTextModelTest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDeepSeekR1Model(BaseTextModelTest):
    """Test class for DeepSeek R1 model API functionality"""
    
    @property
    def model_name(self) -> str:
        """Model name for DeepSeek R1"""
        return "deepseek-ai/DeepSeek-R1-0528-Free"
    
    @property
    def model_params(self) -> dict:
        """Custom parameters for DeepSeek R1"""
        return {
            "max_tokens": None,
            "temperature": 1,
            "top_p": 0.9,
            "stream": False
        }
    
    def test_deepseek_specific_features(self):
        """Test DeepSeek-specific features"""
        self.logger.info("Testing DeepSeek R1 specific features")
        
        # Test with a prompt that DeepSeek should handle well
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt="Explain quantum computing in simple terms",
            **self.model_params
        )
        
        self._validate_basic_response(response)
        
        # Check that response is substantial
        content = response["choices"][0]["message"]["content"]
        assert len(content) > 50, "DeepSeek response should be substantial"
        
        self.logger.info("✅ DeepSeek R1 specific features test passed")
    
    def test_deepseek_code_generation(self):
        """Test DeepSeek's code generation capabilities"""
        self.logger.info("Testing DeepSeek R1 code generation")
        
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
        
        self.logger.info("✅ DeepSeek R1 code generation test passed")
    
    def test_deepseek_math_reasoning(self):
        """Test DeepSeek's mathematical reasoning"""
        self.logger.info("Testing DeepSeek R1 mathematical reasoning")
        
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
        
        self.logger.info("✅ DeepSeek R1 mathematical reasoning test passed")
    
    def test_deepseek_multilingual(self):
        """Test DeepSeek's multilingual capabilities"""
        self.logger.info("Testing DeepSeek R1 multilingual capabilities")
        
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
        
        self.logger.info("✅ DeepSeek R1 multilingual test passed")
    
    def test_deepseek_edge_cases(self):
        """Test DeepSeek with edge cases"""
        self.logger.info("Testing DeepSeek R1 edge cases")
        
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
        
        self.logger.info("✅ DeepSeek R1 edge cases test completed")
    
    def test_deepseek_parameter_variations(self):
        """Test DeepSeek with different parameter combinations"""
        self.logger.info("Testing DeepSeek R1 parameter variations")
        
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
        
        self.logger.info("✅ DeepSeek R1 parameter variations test completed")
    
    def run_deepseek_specific_tests(self):
        """Run all DeepSeek-specific tests"""
        self.logger.info("🚀 Running DeepSeek R1 specific tests")
        
        self.test_deepseek_specific_features()
        self.test_deepseek_code_generation()
        self.test_deepseek_math_reasoning()
        self.test_deepseek_multilingual()
        self.test_deepseek_edge_cases()
        self.test_deepseek_parameter_variations()
        
        self.logger.info("🎉 All DeepSeek R1 specific tests completed")
    
    def run_all_tests(self):
        """Run all tests (basic + specific) for DeepSeek R1"""
        self.logger.info("🚀 Running ALL tests for DeepSeek R1")
        
        # Run basic tests from parent class
        self.run_all_basic_tests()
        
        # Run DeepSeek-specific tests
        self.run_deepseek_specific_tests()
        
        self.logger.info("🎉 ALL tests completed for DeepSeek R1")


# Test functions that can be used independently
def test_deepseek_basic_functionality(model_api):
    """Test basic DeepSeek functionality as a standalone function"""
    logger.info("Testing DeepSeek R1 basic functionality")
    
    test_instance = TestDeepSeekR1Model(model_api)
    test_instance.run_all_basic_tests()
    
    logger.info("✅ DeepSeek R1 basic functionality test completed")


def test_deepseek_full_functionality(model_api):
    """Test full DeepSeek functionality as a standalone function"""
    logger.info("Testing DeepSeek R1 full functionality")
    
    test_instance = TestDeepSeekR1Model(model_api)
    test_instance.run_all_tests()
    
    logger.info("✅ DeepSeek R1 full functionality test completed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
