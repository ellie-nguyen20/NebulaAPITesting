"""
Demo file showcasing the new text model testing framework.
This file demonstrates how to use the BaseTextModelTest classes and utility functions.
"""

import pytest
import logging
from . import (
    TestDeepSeekR1Model,
    TestDeepSeekV3Model,
    TestQwen32BModel,
    TestLlama3370BModel,
    TestAPILimits,
    run_all_tests_for_model,
    run_basic_tests_for_all_models,
    get_all_test_classes
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_individual_model_testing(model_api):
    """Demo individual model testing"""
    logger.info("🚀 Demo: Individual Model Testing")
    
    # Test DeepSeek R1
    logger.info("\n📝 Testing DeepSeek R1 Model...")
    deepseek_r1 = TestDeepSeekR1Model(model_api)
    deepseek_r1.test_basic_connection()
    deepseek_r1.test_simple_prompt()
    
    # Test DeepSeek V3
    logger.info("\n📝 Testing DeepSeek V3 Model...")
    deepseek_v3 = TestDeepSeekV3Model(model_api)
    deepseek_v3.test_basic_connection()
    deepseek_v3.test_simple_prompt()
    
    # Test Qwen 32B
    logger.info("\n📝 Testing Qwen 32B Model...")
    qwen_32b = TestQwen32BModel(model_api)
    qwen_32b.test_basic_connection()
    qwen_32b.test_simple_prompt()
    
    # Test Llama 33B 70B
    logger.info("\n📝 Testing Llama 33B 70B Model...")
    llama_3370b = TestLlama3370BModel(model_api)
    llama_3370b.test_basic_connection()
    llama_3370b.test_simple_prompt()
    
    logger.info("✅ Individual model testing demo completed")


def demo_model_specific_features(model_api):
    """Demo model-specific features"""
    logger.info("\n🚀 Demo: Model-Specific Features")
    
    # Test DeepSeek R1 specific features
    logger.info("\n🔍 Testing DeepSeek R1 specific features...")
    deepseek_r1 = TestDeepSeekR1Model(model_api)
    deepseek_r1.test_deepseek_specific_features()
    deepseek_r1.test_deepseek_code_generation()
    
    # Test Qwen 32B specific features
    logger.info("\n🔍 Testing Qwen 32B specific features...")
    qwen_32b = TestQwen32BModel(model_api)
    qwen_32b.test_qwen_32b_specific_features()
    qwen_32b.test_qwen_32b_code_generation()
    
    logger.info("✅ Model-specific features demo completed")


def demo_api_limits_testing(model_api):
    """Demo API limits testing"""
    logger.info("\n🚀 Demo: API Limits Testing")
    
    limits_tester = TestAPILimits(model_api)
    
    # Test basic functionality first
    logger.info("\n🔍 Testing basic API functionality...")
    limits_tester.test_basic_connection()
    limits_tester.test_simple_prompt()
    
    # Test some limit scenarios (not all to avoid overwhelming the API)
    logger.info("\n🔍 Testing API with different token limits...")
    limits_tester.test_api_token_limits()
    
    logger.info("✅ API limits testing demo completed")


def demo_utility_functions(model_api):
    """Demo utility functions"""
    logger.info("\n🚀 Demo: Utility Functions")
    
    # Get all available test classes
    logger.info("\n📋 Available test classes:")
    test_classes = get_all_test_classes()
    for i, test_class in enumerate(test_classes, 1):
        logger.info(f"   {i}. {test_class.__name__}")
    
    # Run basic tests for all models
    logger.info("\n🔍 Running basic tests for all models...")
    results = run_basic_tests_for_all_models(model_api)
    
    logger.info("\n📊 Results summary:")
    for model_name, result in results.items():
        status_icon = "✅" if "PASSED" in result else "❌"
        logger.info(f"   {status_icon} {model_name}: {result}")
    
    logger.info("✅ Utility functions demo completed")


def demo_custom_model_creation():
    """Demo creating custom model test classes using factory function"""
    logger.info("\n🚀 Demo: Custom Model Creation")
    
    from .base_text_model_test import create_model_test_class
    
    # Create a test class for a custom model
    TestCustomModel = create_model_test_class(
        model_name="custom/example-model",
        custom_params={"temperature": 0.3, "max_tokens": 150}
    )
    
    logger.info(f"✅ Created custom test class: {TestCustomModel.__name__}")
    logger.info(f"   Model: {TestCustomModel().model_name}")
    logger.info(f"   Parameters: {TestCustomModel().model_params}")
    
    # Create another test class with minimal parameters
    TestMinimalModel = create_model_test_class("minimal/test-model")
    logger.info(f"✅ Created minimal test class: {TestMinimalModel.__name__}")
    
    logger.info("✅ Custom model creation demo completed")


def demo_full_test_suite(model_api):
    """Demo running the full test suite for a specific model"""
    logger.info("\n🚀 Demo: Full Test Suite")
    
    # Run all tests for DeepSeek R1
    logger.info("\n🔍 Running full test suite for DeepSeek R1...")
    try:
        run_all_tests_for_model("deepseek-r1", model_api)
        logger.info("✅ Full test suite for DeepSeek R1 completed successfully")
    except Exception as e:
        logger.error(f"❌ Full test suite for DeepSeek R1 failed: {e}")
    
    logger.info("✅ Full test suite demo completed")


def run_complete_demo(model_api):
    """Run the complete demo showcasing all features"""
    logger.info("🎉 Starting Complete Text Model Testing Framework Demo")
    logger.info("=" * 60)
    
    try:
        # Run all demo sections
        demo_individual_model_testing(model_api)
        demo_model_specific_features(model_api)
        demo_api_limits_testing(model_api)
        demo_utility_functions(model_api)
        demo_custom_model_creation()
        demo_full_test_suite(model_api)
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Complete demo finished successfully!")
        logger.info("The text model testing framework is working correctly.")
        
    except Exception as e:
        logger.error(f"\n❌ Demo failed with error: {e}")
        raise


# Pytest test functions
def test_demo_framework_basic(model_api):
    """Test that the demo framework works correctly"""
    logger.info("Testing demo framework basic functionality")
    
    # Test individual model testing
    demo_individual_model_testing(model_api)
    
    # Test utility functions
    demo_utility_functions(model_api)
    
    logger.info("✅ Demo framework basic test completed")


def test_demo_framework_advanced(model_api):
    """Test advanced demo framework features"""
    logger.info("Testing demo framework advanced functionality")
    
    # Test model-specific features
    demo_model_specific_features(model_api)
    
    # Test API limits
    demo_api_limits_testing(model_api)
    
    logger.info("✅ Demo framework advanced test completed")


if __name__ == "__main__":
    # This file can be run directly to see the demo
    logger.info("This is a demo file. Run it through pytest or import the functions.")
    logger.info("Example usage:")
    logger.info("  from tests.serverless_api.text_models.demo_test_framework import run_complete_demo")
    logger.info("  run_complete_demo(model_api)") 