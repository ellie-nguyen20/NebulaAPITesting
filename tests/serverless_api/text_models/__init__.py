"""
Text Models Testing Module

This module provides a comprehensive testing framework for text models using the BaseTextModelTest class.
All test classes inherit from BaseTextModelTest and provide consistent testing patterns.

Available Test Classes:
- TestDeepSeekR1Model: Tests for DeepSeek R1 model
- TestDeepSeekV3Model: Tests for DeepSeek V3 model  
- TestQwen32BModel: Tests for Qwen 32B model
- TestLlama3370BModel: Tests for Llama 33B 70B model
- TestAPILimits: Tests for API limits and stress testing

Usage:
    from tests.serverless_api.text_models import TestDeepSeekR1Model
    
    # Create test instance
    test_instance = TestDeepSeekR1Model(model_api)
    
    # Run basic tests
    test_instance.run_all_basic_tests()
    
    # Run all tests (basic + specific)
    test_instance.run_all_tests()
"""

from .base_text_model_test import BaseTextModelTest, create_model_test_class
from .test_deepseek_r1_0528 import TestDeepSeekR1Model
from .test_deepseek_v3_0324 import TestDeepSeekV3Model
from .test_Qwen_32B import TestQwen32BModel
from .test_Llama33_70B import TestLlama3370BModel
# from .test_limit import TestAPILimits

__all__ = [
    # Base classes
    "BaseTextModelTest",
    "create_model_test_class",
    
    # Model test classes
    "TestDeepSeekR1Model",
    "TestDeepSeekV3Model", 
    "TestQwen32BModel",
    "TestLlama3370BModel",
    "TestAPILimits",
]

# Convenience function to get all available test classes
def get_all_test_classes():
    """Get all available test classes"""
    return [
        TestDeepSeekR1Model,
        TestDeepSeekV3Model,
        TestQwen32BModel,
        TestLlama3370BModel,
        # TestAPILimits,
    ]

# Convenience function to run all tests for a specific model
def run_all_tests_for_model(model_name: str, model_api):
    """Run all tests for a specific model by name"""
    model_map = {
        "deepseek-r1": TestDeepSeekR1Model,
        "deepseek-v3": TestDeepSeekV3Model,
        "qwen-32b": TestQwen32BModel,
        "llama-33b-70b": TestLlama3370BModel,
        # "api-limits": TestAPILimits,
    }
    
    if model_name not in model_map:
        raise ValueError(f"Unknown model: {model_name}. Available models: {list(model_map.keys())}")
    
    test_class = model_map[model_name]
    test_instance = test_class(model_api)
    test_instance.run_all_tests()
    
    return test_instance

# Convenience function to run basic tests for all models
def run_basic_tests_for_all_models(model_api):
    """Run basic tests for all available models"""
    results = {}
    
    for test_class in get_all_test_classes():
        try:
            test_instance = test_class(model_api)
            test_instance.run_all_basic_tests()
            results[test_class.__name__] = "PASSED"
        except Exception as e:
            results[test_class.__name__] = f"FAILED: {str(e)}"
    
    return results

# Convenience function to get model information
def get_model_info():
    """Get information about all available models"""
    model_info = {
        "deepseek-r1": {
            "name": "DeepSeek R1",
            "model_id": "deepseek-ai/DeepSeek-R1-0528-Free",
            "description": "DeepSeek R1 52.8B parameter model",
            "test_class": TestDeepSeekR1Model,
            "features": ["text generation", "code generation", "mathematical reasoning", "multilingual"]
        },
        "deepseek-v3": {
            "name": "DeepSeek V3",
            "model_id": "deepseek-ai/DeepSeek-V3-0324-Free",
            "description": "DeepSeek V3 32.4B parameter model",
            "test_class": TestDeepSeekV3Model,
            "features": ["text generation", "code generation", "mathematical reasoning", "multilingual"]
        },
        "qwen-32b": {
            "name": "Qwen 32B",
            "model_id": "Qwen/QwQ-32B",
            "description": "Qwen 32B parameter model",
            "test_class": TestQwen32BModel,
            "features": ["text generation", "code generation", "mathematical reasoning", "multilingual"]
        },
        "llama-33b-70b": {
            "name": "Llama 33B 70B",
            "model_id": "meta-llama/Llama-3.3-70B-Instruct",
            "description": "Meta's Llama 3.3 70B parameter model",
            "test_class": TestLlama3370BModel,
            "features": ["text generation", "code generation", "mathematical reasoning", "multilingual"]
        },
        "api-limits": {
            "name": "API Limits",
            "model_id": "deepseek-ai/DeepSeek-R1-Free",
            "description": "Testing framework for API limits and stress testing",
            "test_class": TestAPILimits,
            "features": ["rate limiting", "concurrent requests", "prompt limits", "token limits"]
        }
    }
    
    return model_info

# Convenience function to create a test runner for multiple models
def create_test_runner(model_names: list, model_api):
    """Create a test runner for multiple models"""
    class MultiModelTestRunner:
        def __init__(self, model_names, model_api):
            self.model_names = model_names
            self.model_api = model_api
            self.model_info = get_model_info()
        
        def run_basic_tests(self):
            """Run basic tests for selected models"""
            results = {}
            for model_name in self.model_names:
                if model_name in self.model_info:
                    try:
                        test_class = self.model_info[model_name]["test_class"]
                        test_instance = test_class(self.model_api)
                        test_instance.run_all_basic_tests()
                        results[model_name] = "PASSED"
                    except Exception as e:
                        results[model_name] = f"FAILED: {str(e)}"
                else:
                    results[model_name] = "UNKNOWN MODEL"
            return results
        
        def run_full_tests(self):
            """Run full tests for selected models"""
            results = {}
            for model_name in self.model_names:
                if model_name in self.model_info:
                    try:
                        test_class = self.model_info[model_name]["test_class"]
                        test_instance = test_class(self.model_api)
                        test_instance.run_all_tests()
                        results[model_name] = "PASSED"
                    except Exception as e:
                        results[model_name] = f"FAILED: {str(e)}"
                else:
                    results[model_name] = "UNKNOWN MODEL"
            return results
    
    return MultiModelTestRunner(model_names, model_api)
