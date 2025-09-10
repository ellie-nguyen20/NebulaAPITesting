import pytest
import logging
from api_clients.multimodal_models import MultimodalModelsAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gemini_2_0_flash_simple(config, api_key_scope_session):
    logger.info("🚀 Starting Gemini 2.0 Flash test with simple prompt")
    
    try:
        multimodal_config = {
            "chat_completions_url": config["chat_completions_url"],
            "api_key": api_key_scope_session
        }
        multimodal_api = MultimodalModelsAPI(multimodal_config)
        logger.info("✅ MultimodalModelsAPI instance created successfully")
        
        response = multimodal_api.call_model(
            model_name="gemini-2.0-flash",
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
        logger.info(f"📝 Gemini 2.0 Flash response: {content}")
        
        assert len(content) > 0, "Response content should not be empty"
        assert isinstance(content, str), "Response content should be a string"
        
        logger.info("✅ Gemini 2.0 Flash test completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Gemini 2.0 Flash test failed: {e}")
        raise
