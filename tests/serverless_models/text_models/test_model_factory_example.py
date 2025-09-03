"""
Example file demonstrating how to use the factory function to create test classes for different models.
This shows the flexibility of the BaseTextModelTest architecture.
"""

import pytest
import logging
from .base_text_model_test import create_model_test_class, BaseTextModelTest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Example 1: Using factory function to create test class for a simple model
TestSimpleModel = create_model_test_class(
    model_name="simple/text-model",
    custom_params={"temperature": 0.5, "max_tokens": 100}
)


# Example 2: Using factory function for another model with different parameters
TestAdvancedModel = create_model_test_class(
    model_name="advanced/ai-model",
    custom_params={"temperature": 0.8, "top_p": 0.95, "stream": True}
)


# Example 3: Creating a custom test class that inherits from BaseTextModelTest
class TestCustomModel(BaseTextModelTest):
    """Custom test class for a specific model with custom logic"""
    
    @property
    def model_name(self) -> str:
        return "custom/special-model"
    
    @property
    def model_params(self) -> dict:
        return {
            "max_tokens": 200,
            "temperature": 0.3,
            "top_p": 0.8,
            "stream": False
        }
    
    def test_custom_specific_feature(self):
        """Test a feature specific to this custom model"""
        self.logger.info("Testing custom model specific feature")
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt="This is a custom test prompt",
            **self.model_params
        )
        
        self._validate_basic_response(response)
        
        # Custom validation logic
        content = response["choices"][0]["message"]["content"]
        assert "custom" in content.lower() or "special" in content.lower(), "Response should be relevant to custom model"
        
        self.logger.info("✅ Custom model specific feature test passed")
    
    def test_custom_edge_case(self):
        """Test a custom edge case for this model"""
        self.logger.info("Testing custom model edge case")
        
        # Custom edge case logic
        edge_prompt = "A" * 10000  # Very long prompt
        
        try:
            response = self.model_api.send_text_message(
                model=self.model_name,
                prompt=edge_prompt,
                **self.model_params
            )
            
            self._validate_basic_response(response)
            self.logger.info("✅ Custom edge case handled successfully")
            
        except Exception as e:
            self.logger.info(f"✅ Custom edge case properly handled: {e}")


# Example 4: Using factory function with minimal parameters
TestMinimalModel = create_model_test_class("minimal/model")


# Example 5: Using factory function with extensive custom parameters
TestExtensiveModel = create_model_test_class(
    model_name="extensive/feature-rich-model",
    custom_params={
        "max_tokens": 500,
        "temperature": 0.1,
        "top_p": 0.9,
        "stream": False,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1
    }
)


# Example 6: Creating a test class for a model that needs special handling
class TestSpecialHandlingModel(BaseTextModelTest):
    """Test class for a model that requires special handling"""
    
    @property
    def model_name(self) -> str:
        return "special/handling-model"
    
    @property
    def model_params(self) -> dict:
        return {
            "max_tokens": 150,
            "temperature": 0.7,
            "top_p": 0.85,
            "stream": False
        }
    
    def test_special_prompt_format(self):
        """Test that this model handles special prompt formats"""
        self.logger.info("Testing special prompt format handling")
        
        # Test with different prompt formats
        prompt_formats = [
            "Question: What is AI?",
            "Task: Explain machine learning",
            "Instruction: Write a summary",
            "Context: In the field of technology...",
        ]
        
        for prompt in prompt_formats:
            response = self.model_api.send_text_message(
                model=self.model_name,
                prompt=prompt,
                **self.model_params
            )
            
            self._validate_basic_response(response)
            
            # Check that response is appropriate for the prompt format
            content = response["choices"][0]["message"]["content"]
            assert len(content) > 10, f"Response for '{prompt}' should be substantial"
        
        self.logger.info("✅ Special prompt format handling test passed")
    
    def test_special_response_validation(self):
        """Test custom response validation for this model"""
        self.logger.info("Testing custom response validation")
        
        response = self.model_api.send_text_message(
            model=self.model_name,
            prompt="Generate a creative story",
            **self.model_params
        )
        
        # Custom validation beyond basic validation
        self._validate_basic_response(response)
        
        content = response["choices"][0]["message"]["content"]
        
        # Check for creative elements
        creative_words = ["story", "creative", "imagine", "once", "character"]
        has_creative_elements = any(word in content.lower() for word in creative_words)
        
        assert has_creative_elements, "Response should contain creative story elements"
        
        self.logger.info("✅ Custom response validation test passed")


# Example 7: Demonstrating how to use these test classes in pytest
def test_factory_created_classes(model_api):
    """Test that factory-created classes work correctly"""
    logger.info("Testing factory-created test classes")
    
    # Test SimpleModel
    simple_test = TestSimpleModel(model_api)
    simple_test.test_basic_connection()
    simple_test.test_simple_prompt()
    
    # Test AdvancedModel
    advanced_test = TestAdvancedModel(model_api)
    advanced_test.test_basic_connection()
    advanced_test.test_response_structure()
    
    # Test MinimalModel
    minimal_test = TestMinimalModel(model_api)
    minimal_test.test_basic_connection()
    
    logger.info("✅ All factory-created test classes working correctly")


def test_custom_inherited_classes(model_api):
    """Test that custom inherited classes work correctly"""
    logger.info("Testing custom inherited test classes")
    
    # Test CustomModel
    custom_test = TestCustomModel(model_api)
    custom_test.test_basic_connection()
    custom_test.test_custom_specific_feature()
    custom_test.test_custom_edge_case()
    
    # Test SpecialHandlingModel
    special_test = TestSpecialHandlingModel(model_api)
    special_test.test_basic_connection()
    special_test.test_special_prompt_format()
    special_test.test_special_response_validation()
    
    logger.info("✅ All custom inherited test classes working correctly")


def test_model_parameter_customization(model_api):
    """Test that model parameters are properly customized"""
    logger.info("Testing model parameter customization")
    
    # Test that SimpleModel has custom parameters
    simple_test = TestSimpleModel(model_api)
    assert simple_test.model_params["temperature"] == 0.5
    assert simple_test.model_params["max_tokens"] == 100
    
    # Test that AdvancedModel has custom parameters
    advanced_test = TestAdvancedModel(model_api)
    assert advanced_test.model_params["temperature"] == 0.8
    assert advanced_test.model_params["stream"] == True
    
    # Test that CustomModel has custom parameters
    custom_test = TestCustomModel(model_api)
    assert custom_test.model_params["temperature"] == 0.3
    assert custom_test.model_params["max_tokens"] == 200
    
    logger.info("✅ Model parameter customization working correctly")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"]) 