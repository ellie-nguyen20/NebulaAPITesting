# tests/run_all_model_tests.py
#!/usr/bin/env python3
"""
Main test runner for all model tests.
Demonstrates how to use the ModelTestFactory to run tests efficiently.
"""

import sys
import os
import logging
import argparse
from typing import Dict, Any

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.model_test_factory import model_test_factory
from tests.base_model_test import BaseModelTest

# Import all model test classes
from tests.serverless_api.text_models.test_deepseek_r1_refactored import TestDeepSeekR1
from tests.serverless_api.multimodal_models.test_gemini_20_flash_refactored import TestGemini20Flash

def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('model_tests.log')
        ]
    )

def load_config() -> Dict[str, Any]:
    """Load test configuration."""
    # This would typically load from config.yaml or environment variables
    # For demonstration, using hardcoded values
    return {
        "model_base_url": "https://dev-llm-proxy.nebulablock.com/v1",
        "api_key": os.getenv("NEBULA_API_KEY", "your_api_key_here"),
        "timeout": 30
    }

def register_all_models() -> None:
    """Register all available model test classes with the factory."""
    logger = logging.getLogger(__name__)
    
    # Register text models
    model_test_factory.register_model("deepseek-r1", TestDeepSeekR1)
    logger.info("Registered DeepSeek R1 model test")
    
    # Register multimodal models
    model_test_factory.register_model("gemini-20-flash", TestGemini20Flash)
    logger.info("Registered Gemini 2.0 Flash model test")
    
    # You can add more models here as you create them
    
    logger.info(f"Total registered models: {len(model_test_factory.list_registered_models())}")

def run_tests_by_category(config: Dict[str, Any], category: str = None) -> Dict[str, Any]:
    """
    Run tests for specific category or all models.
    
    Args:
        config: Test configuration
        category: Optional category to test (text, multimodal, embedding)
        
    Returns:
        Test results dictionary
    """
    logger = logging.getLogger(__name__)
    
    if category:
        logger.info(f"Running tests for category: {category}")
        results = model_test_factory.run_category_tests(category, config)
    else:
        logger.info("Running tests for all models")
        results = model_test_factory.run_all_tests(config)
    
    return results

def print_results(results: Dict[str, Any]) -> None:
    """Print test results in a formatted way."""
    print("\n" + "="*60)
    print("MODEL TEST RESULTS")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for model_name, result in results.items():
        status = result["status"]
        if status == "passed":
            passed += 1
            print(f"✅ {model_name}: PASSED")
        else:
            failed += 1
            print(f"❌ {model_name}: FAILED")
            if result["error"]:
                print(f"   Error: {result['error']}")
    
    print("-"*60)
    print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")
    print("="*60)

def main():
    """Main function to run the test suite."""
    parser = argparse.ArgumentParser(description="Run model tests")
    parser.add_argument(
        "--category", 
        choices=["text", "multimodal", "embedding"],
        help="Run tests for specific category only"
    )
    parser.add_argument(
        "--log-level", 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging level"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all registered models and exit"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate model registrations and exit"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Register all models
        register_all_models()
        
        # List models if requested
        if args.list_models:
            print("\nRegistered Models:")
            for model_name in model_test_factory.list_registered_models():
                print(f"  - {model_name}")
            
            print("\nModel Categories:")
            categories = model_test_factory.get_model_categories()
            for category, models in categories.items():
                print(f"  {category}: {', '.join(models)}")
            return
        
        # Validate registrations if requested
        if args.validate:
            warnings = model_test_factory.validate_model_registration()
            if warnings:
                print("\nValidation Warnings:")
                for warning in warnings:
                    print(f"  ⚠️  {warning}")
            else:
                print("\n✅ All model registrations are valid")
            return
        
        # Check if API key is set
        if config["api_key"] == "your_api_key_here":
            logger.error("Please set NEBULA_API_KEY environment variable")
            sys.exit(1)
        
        # Run tests
        results = run_tests_by_category(config, args.category)
        
        # Print results
        print_results(results)
        
        # Exit with appropriate code
        failed_count = sum(1 for r in results.values() if r["status"] == "failed")
        sys.exit(failed_count)
        
    except KeyboardInterrupt:
        logger.info("Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 