import pytest
import logging
from api_clients.text_models import TextModelsAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_engineer_tier1_cannot_use_any_deepseek_free(login_as_user):
    """Test that Engineer Tier 1 cannot use any DeepSeek Free models."""
    user_config = login_as_user("Member9")
    
    # Test all 3 DeepSeek Free models
    models = ["deepseek-r1-free", "deepseek-v3-0324-free", "deepseek-r1-0528-free"]
    
    for model in models:
        try:
            text_api = TextModelsAPI(user_config)
            response = text_api.call_model(
                model_name=model,
                prompt="Hello, can you help me?",
                system_message="You are a helpful assistant."
            )
            assert False, f"Engineer Tier 1 should not be able to use {model}"
            
        except Exception as e:
            error_message = str(e)
            expected_error_phrases = [
                "Authentication Error", "Invalid proxy server token passed", "not found in db",
                "Create key via", "token_not_found_in_db", "key=", "code", "401"
            ]
            
            error_lower = error_message.lower()
            found_phrases = [phrase for phrase in expected_error_phrases if phrase.lower() in error_lower]
            
            assert len(found_phrases) >= 4, f"Expected at least 4 error phrases for {model}, found {len(found_phrases)}: {found_phrases}. Error: {error_message}"

def test_engineer_tier1_specific_error_message(login_as_user):
    """Test that Engineer Tier 1 gets specific error message for DeepSeek models."""
    user_config = login_as_user("Member9")
    
    try:
        text_api = TextModelsAPI(user_config)
        response = text_api.call_model(
            model_name="deepseek-r1-free",
            prompt="Hello, can you help me?",
            system_message="You are a helpful assistant."
        )
        assert False, "Engineer Tier 1 should not be able to use DeepSeek R1 Free model"
        
    except Exception as e:
        error_message = str(e)
        expected_error_phrases = [
            "Authentication Error", "Invalid proxy server token passed", "not found in db",
            "Create key via", "token_not_found_in_db", "key=", "code", "401"
        ]
        
        error_lower = error_message.lower()
        found_phrases = [phrase for phrase in expected_error_phrases if phrase.lower() in error_lower]
        
        assert len(found_phrases) >= 4, f"Expected at least 4 error phrases, found {len(found_phrases)}: {found_phrases}. Error: {error_message}"

def test_engineer_tier2_can_use_all_deepseek_free(login_as_user):
    """Test that Engineer Tier 2 can use all DeepSeek Free models."""
    user_config = login_as_user("Member8")
    
    text_api = TextModelsAPI(user_config)
    
    # Test all 3 DeepSeek Free models
    models = ["deepseek-r1-free", "deepseek-v3-0324-free", "deepseek-r1-0528-free"]
    
    for model in models:
        response = text_api.call_model(
            model_name=model,
            prompt="Hello, can you help me?",
            system_message="You are a helpful assistant."
        )
        
        assert response is not None, f"Response should not be None for {model}"
        assert "choices" in response, f"Response should contain 'choices' field for {model}. Got: {response}"
        assert len(response["choices"]) > 0, f"Response should have at least one choice for {model}"
        
        content = response["choices"][0]["message"]["content"]
        assert len(content) > 0, f"Response content should not be empty for {model}"
        assert isinstance(content, str), f"Response content should be a string for {model}"

def test_engineer_tier3_can_use_all_deepseek_free(login_as_user):
    """Test that Engineer Tier 3 can use all DeepSeek Free models."""
    user_config = login_as_user("Member7")
    
    text_api = TextModelsAPI(user_config)
    
    # Test all 3 DeepSeek Free models
    models = ["deepseek-r1-free", "deepseek-v3-0324-free", "deepseek-r1-0528-free"]
    
    for model in models:
        response = text_api.call_model(
            model_name=model,
            prompt="Hello, can you help me?",
            system_message="You are a helpful assistant."
        )
        
        assert response is not None, f"Response should not be None for {model}"
        assert "choices" in response, f"Response should contain 'choices' field for {model}. Got: {response}"
        assert len(response["choices"]) > 0, f"Response should have at least one choice for {model}"
        
        content = response["choices"][0]["message"]["content"]
        assert len(content) > 0, f"Response content should not be empty for {model}"
        assert isinstance(content, str), f"Response content should be a string for {model}"

def test_expert_tier1_can_use_all_deepseek_free(login_as_user):
    """Test that Expert Tier 1 (Member4) can use all DeepSeek Free models."""
    user_config = login_as_user("Member4")
    
    text_api = TextModelsAPI(user_config)
    
    # Test all 3 DeepSeek Free models
    models = ["deepseek-r1-free", "deepseek-v3-0324-free", "deepseek-r1-0528-free"]
    
    for model in models:
        response = text_api.call_model(
            model_name=model,
            prompt="Hello, can you help me?",
            system_message="You are a helpful assistant."
        )
        
        assert response is not None, f"Response should not be None for {model}"
        assert "choices" in response, f"Response should contain 'choices' field for {model}. Got: {response}"
        assert len(response["choices"]) > 0, f"Response should have at least one choice for {model}"
        
        content = response["choices"][0]["message"]["content"]
        assert len(content) > 0, f"Response content should not be empty for {model}"
        assert isinstance(content, str), f"Response content should be a string for {model}"

def test_expert_tier2_can_use_all_deepseek_free(login_as_user):
    """Test that Expert Tier 2 (Ellie) can use all DeepSeek Free models."""
    user_config = login_as_user("Ellie")
    
    text_api = TextModelsAPI(user_config)
    
    # Test all 3 DeepSeek Free models
    models = ["deepseek-r1-free", "deepseek-v3-0324-free", "deepseek-r1-0528-free"]
    
    for model in models:
        response = text_api.call_model(
            model_name=model,
            prompt="Hello, can you help me?",
            system_message="You are a helpful assistant."
        )
        
        assert response is not None, f"Response should not be None for {model}"
        assert "choices" in response, f"Response should contain 'choices' field for {model}. Got: {response}"
        assert len(response["choices"]) > 0, f"Response should have at least one choice for {model}"
        
        content = response["choices"][0]["message"]["content"]
        assert len(content) > 0, f"Response content should not be empty for {model}"
        assert isinstance(content, str), f"Response content should be a string for {model}"

def test_tier_hierarchy_access_control(login_as_user):
    """Test tier hierarchy: Engineer Tier 1 blocked, others allowed."""
    # Test Engineer Tier 1 (should be blocked)
    try:
        user_config = login_as_user("Member9")
        text_api = TextModelsAPI(user_config)
        response = text_api.call_model(
            model_name="deepseek-r1-free",
            prompt="Hello",
            system_message="You are a helpful assistant."
        )
        assert False, "Engineer Tier 1 should be blocked"
    except Exception:
        pass  # Expected to fail
    
    # Test Engineer Tier 2 (should be allowed)
    user_config = login_as_user("Member8")
    text_api = TextModelsAPI(user_config)
    response = text_api.call_model(
        model_name="deepseek-r1-free",
        prompt="Hello",
        system_message="You are a helpful assistant."
    )
    assert response is not None, "Engineer Tier 2 should be allowed"

def test_all_high_tier_users_can_access_deepseek_free(login_as_user):
    """Test that all high tier users can access DeepSeek Free models."""
    high_tier_users = ["Member8", "Member7", "Member4", "Ellie"]
    
    for user in high_tier_users:
        user_config = login_as_user(user)
        text_api = TextModelsAPI(user_config)
        
        response = text_api.call_model(
            model_name="deepseek-r1-free",
            prompt="Hello",
            system_message="You are a helpful assistant."
        )
        
        assert response is not None, f"User {user} should be allowed to use DeepSeek Free models"
        assert "choices" in response, f"User {user} should get valid response"
        assert len(response["choices"]) > 0, f"User {user} should get at least one choice"