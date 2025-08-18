# tests/model_test_factory.py
from typing import Dict, Any, Type, List
from .base_model_test import BaseModelTest
import logging

class ModelTestFactory:
    """
    Factory class for creating and managing model tests.
    Makes it easy to add new models and maintain test consistency.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._model_tests: Dict[str, Type[BaseModelTest]] = {}
        self._model_configs: Dict[str, Dict[str, Any]] = {}
    
    def register_model(
        self, 
        model_name: str, 
        test_class: Type[BaseModelTest],
        config: Dict[str, Any] = None
    ) -> None:
        """
        Register a model test class.
        
        Args:
            model_name: Unique identifier for the model
            test_class: Test class that inherits from BaseModelTest
            config: Optional model-specific configuration
        """
        if not issubclass(test_class, BaseModelTest):
            raise ValueError(f"Test class must inherit from BaseModelTest")
        
        self._model_tests[model_name] = test_class
        if config:
            self._model_configs[model_name] = config
        
        self.logger.info(f"Registered model test: {model_name}")
    
    def get_model_test(self, model_name: str) -> Type[BaseModelTest]:
        """
        Get a registered model test class.
        
        Args:
            model_name: Model identifier
            
        Returns:
            Model test class
            
        Raises:
            KeyError: If model is not registered
        """
        if model_name not in self._model_tests:
            raise KeyError(f"Model '{model_name}' not registered. Available models: {list(self._model_tests.keys())}")
        
        return self._model_tests[model_name]
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """
        Get model-specific configuration.
        
        Args:
            model_name: Model identifier
            
        Returns:
            Model configuration dictionary
        """
        return self._model_configs.get(model_name, {})
    
    def list_registered_models(self) -> List[str]:
        """
        Get list of all registered models.
        
        Returns:
            List of model names
        """
        return list(self._model_tests.keys())
    
    def get_model_categories(self) -> Dict[str, List[str]]:
        """
        Categorize models by type (text, multimodal, embedding).
        
        Returns:
            Dictionary mapping categories to model lists
        """
        categories = {
            "text": [],
            "multimodal": [],
            "embedding": []
        }
        
        for model_name, test_class in self._model_tests.items():
            # Create a temporary instance to check model type
            try:
                temp_config = {"model_base_url": "dummy", "api_key": "dummy"}
                temp_instance = test_class(temp_config)
                
                if "embedding" in model_name.lower():
                    categories["embedding"].append(model_name)
                elif temp_instance.is_multimodal():
                    categories["multimodal"].append(model_name)
                else:
                    categories["text"].append(model_name)
                    
            except Exception as e:
                self.logger.warning(f"Could not categorize model {model_name}: {e}")
                categories["text"].append(model_name)  # Default to text
        
        return categories
    
    def run_all_tests(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run tests for all registered models.
        
        Args:
            config: Test configuration
            
        Returns:
            Dictionary with test results for each model
        """
        results = {}
        
        for model_name in self.list_registered_models():
            try:
                self.logger.info(f"Running tests for model: {model_name}")
                
                test_class = self.get_model_test(model_name)
                test_instance = test_class(config)
                
                # Run main test
                test_instance.test_model_api(config)
                
                # Run additional tests
                test_instance.test_model_info(config)
                test_instance.test_embeddings(config)
                
                results[model_name] = {"status": "passed", "error": None}
                self.logger.info(f"Model {model_name} tests completed successfully")
                
            except Exception as e:
                results[model_name] = {"status": "failed", "error": str(e)}
                self.logger.error(f"Model {model_name} tests failed: {e}")
        
        return results
    
    def run_category_tests(self, category: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run tests for models in a specific category.
        
        Args:
            category: Category name (text, multimodal, embedding)
            config: Test configuration
            
        Returns:
            Dictionary with test results
        """
        categories = self.get_model_categories()
        
        if category not in categories:
            raise ValueError(f"Invalid category '{category}'. Available: {list(categories.keys())}")
        
        category_models = categories[category]
        results = {}
        
        for model_name in category_models:
            try:
                self.logger.info(f"Running {category} tests for model: {model_name}")
                
                test_class = self.get_model_test(model_name)
                test_instance = test_class(config)
                
                test_instance.test_model_api(config)
                results[model_name] = {"status": "passed", "error": None}
                
            except Exception as e:
                results[model_name] = {"status": "failed", "error": str(e)}
                self.logger.error(f"Model {model_name} tests failed: {e}")
        
        return results
    
    def validate_model_registration(self) -> List[str]:
        """
        Validate all registered models for potential issues.
        
        Returns:
            List of validation warnings
        """
        warnings = []
        
        for model_name, test_class in self._model_tests.items():
            try:
                # Check if test class can be instantiated
                temp_config = {"model_base_url": "dummy", "api_key": "dummy"}
                temp_instance = test_class(temp_config)
                
                # Check required methods
                if not hasattr(temp_instance, 'get_model_name'):
                    warnings.append(f"Model {model_name}: Missing get_model_name method")
                
                # Check if model name is consistent
                try:
                    declared_name = temp_instance.get_model_name()
                    if declared_name != model_name:
                        warnings.append(f"Model {model_name}: Declared name '{declared_name}' doesn't match registration")
                except Exception as e:
                    warnings.append(f"Model {model_name}: get_model_name method failed: {e}")
                
            except Exception as e:
                warnings.append(f"Model {model_name}: Instantiation failed: {e}")
        
        return warnings

# Global factory instance
model_test_factory = ModelTestFactory() 