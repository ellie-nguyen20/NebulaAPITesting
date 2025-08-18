# tests/serverless_api/multimodal_models/test_gemini_20_flash_refactored.py
import pytest
import os
from tests.base_model_test import BaseModelTest

class TestGemini20Flash(BaseModelTest):
    """
    Refactored test class for Gemini 2.0 Flash model using the base class.
    Demonstrates multimodal testing capabilities.
    """
    
    def get_model_name(self) -> str:
        """Return the model identifier."""
        return "gemini/gemini-2.0-flash"
    
    def get_test_cases(self) -> list:
        """Override test cases for this specific model."""
        return [
            ("TC_00_CheckConnection", "Is this API working correctly?", 200),
            ("TC_01_ValidRequest", "Hello, how are you?", 200),
            ("TC_02_LongPrompt", "A" * 5000, 200),
            ("TC_03_SpecialCharacters", "What is 2+2? 😊", 200),
            ("TC_04_EmptyPrompt", "", 400),
            ("TC_05_InvalidAPIKey", "Hello", 401),
            ("TC_06_NoAPIKey", "Hello", 401),
        ]
    
    def get_model_params(self) -> dict:
        """Override model parameters if needed."""
        return {
            "max_tokens": None,
            "temperature": 1,
            "top_p": 0.9,
            "stream": False,
        }
    
    def is_multimodal(self) -> bool:
        """Gemini 2.0 Flash supports multimodal input."""
        return True
    
    def get_test_images(self) -> list:
        """Get test images for multimodal testing."""
        # You can add actual image files to the data/images directory
        test_images = [
            # Example image paths - adjust based on your actual test images
            "data/images/test_image_1.jpg",
            "data/images/test_image_2.png",
        ]
        
        # Filter to only include existing files
        existing_images = [img for img in test_images if os.path.exists(img)]
        
        if not existing_images:
            # Fallback to sample URLs if no local images
            existing_images = [
                "https://picsum.photos/200/200",  # Sample image service
            ]
        
        return existing_images
    
    def test_multimodal_capabilities(self, config: dict) -> None:
        """
        Test Gemini's multimodal capabilities specifically.
        This method demonstrates how to add multimodal-specific tests.
        """
        self.__init__(config)
        
        images = self.get_test_images()
        if not images:
            pytest.skip("No test images available for multimodal testing")
        
        # Test with image and text
        response = self.model_api.send_multimodal_message(
            model=self.get_model_name(),
            prompt="Describe what you see in this image",
            images=images[:1],  # Use first image
            **self.get_model_params()
        )
        
        # Validate response
        self.validate_response("Gemini_Multimodal", response)
        
        # Check if response acknowledges the image
        content = response["choices"][0]["message"]["content"]
        assert len(content) > 20, "Multimodal response should be substantial"
        
        self.logger.info("Gemini multimodal capabilities test passed")
    
    def test_image_analysis(self, config: dict) -> None:
        """
        Test Gemini's image analysis capabilities.
        """
        self.__init__(config)
        
        images = self.get_test_images()
        if not images:
            pytest.skip("No test images available")
        
        # Test with specific image analysis prompt
        response = self.model_api.send_multimodal_message(
            model=self.get_model_name(),
            prompt="Analyze the colors, objects, and composition in this image",
            images=images[:1],
            **self.get_model_params()
        )
        
        self.validate_response("Gemini_ImageAnalysis", response)
        
        content = response["choices"][0]["message"]["content"]
        # Check if response contains analysis-related keywords
        analysis_keywords = ["color", "object", "composition", "image", "see"]
        has_analysis = any(keyword.lower() in content.lower() for keyword in analysis_keywords)
        
        assert has_analysis, "Response should contain image analysis content"
        self.logger.info("Gemini image analysis test passed")
    
    def test_multiple_images(self, config: dict) -> None:
        """
        Test Gemini's ability to handle multiple images.
        """
        self.__init__(config)
        
        images = self.get_test_images()
        if len(images) < 2:
            pytest.skip("Need at least 2 test images for multiple image testing")
        
        # Test with multiple images
        response = self.model_api.send_multimodal_message(
            model=self.get_model_name(),
            prompt="Compare these two images and describe the differences",
            images=images[:2],  # Use first two images
            **self.get_model_params()
        )
        
        self.validate_response("Gemini_MultipleImages", response)
        
        content = response["choices"][0]["message"]["content"]
        assert len(content) > 30, "Multiple image response should be detailed"
        
        self.logger.info("Gemini multiple images test passed")

# Test functions that pytest will discover
def test_gemini_20_flash_api(config):
    """Main test function for Gemini 2.0 Flash."""
    test_instance = TestGemini20Flash(config)
    test_instance.test_model_api(config)

def test_gemini_20_flash_info(config):
    """Test getting Gemini 2.0 Flash model information."""
    test_instance = TestGemini20Flash(config)
    test_instance.test_model_info(config)

def test_gemini_20_flash_multimodal(config):
    """Test Gemini's multimodal capabilities."""
    test_instance = TestGemini20Flash(config)
    test_instance.test_multimodal_capabilities(config)

def test_gemini_20_flash_image_analysis(config):
    """Test Gemini's image analysis capabilities."""
    test_instance = TestGemini20Flash(config)
    test_instance.test_image_analysis(config)

def test_gemini_20_flash_multiple_images(config):
    """Test Gemini's multiple image handling."""
    test_instance = TestGemini20Flash(config)
    test_instance.test_multiple_images(config) 