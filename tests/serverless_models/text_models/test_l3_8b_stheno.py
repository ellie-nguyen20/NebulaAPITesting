import pytest
import logging
from api_clients.text_models import TextModelsAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_l3_8b_stheno_simple(config, api_key_scope_session):
    logger.info("🚀 Starting L3-8B-Stheno text test with simple prompt")
    
    try:
        text_config = {
            "chat_completions_url": config["chat_completions_url"],
            "api_key": api_key_scope_session
        }
        text_api = TextModelsAPI(text_config)
        logger.info("✅ TextModelsAPI instance created successfully")
        
        response = text_api.call_model(
            model_name="l3-8b-stheno",
            prompt="Is Montreal a thriving hub for the AI industry?",
            system_message="You are a helpful assistant."
        )
        
        assert response is not None, "Response should not be None"
        
        if "error" in response:
            error_msg = f"API Error: {response['error']}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        assert "choices" in response, f"Response should contain 'choices' field. Got: {response}"
        assert len(response["choices"]) > 0, "Response should have at least one choice"
        
        content = response["choices"][0]["message"]["content"]
        logger.info(f"📝 L3-8B-Stheno text response: {content}")
        
        assert len(content) > 0, "Response content should not be empty"
        assert isinstance(content, str), "Response content should be a string"
        
        logger.info("✅ L3-8B-Stheno text test completed successfully")
        
    except Exception as e:
        logger.error(f"❌ L3-8B-Stheno text test failed: {e}")
        raise
