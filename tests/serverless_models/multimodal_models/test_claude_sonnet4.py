import pytest
import logging
from api_clients.multimodal_models import MultimodalModelsAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_new_claude_sonnet4(config, api_key_scope_session):
    logger.info("🚀 Starting Claude Sonnet 4 test with simple prompt")
    
    try:
        multimodal_config = {
            "chat_completions_url": config["chat_completions_url"],
            "api_key": api_key_scope_session
        }
        multimodal_api = MultimodalModelsAPI(multimodal_config)
        logger.info("✅ MultimodalModelsAPI instance created successfully")
        
        response = multimodal_api.call_model(
            model_name="claude-sonnet-4",
            prompt="Hello",
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
        logger.info(f"📝 Claude Sonnet 4 response: {content}")
        
        assert len(content) > 0, "Response content should not be empty"
        assert isinstance(content, str), "Response content should be a string"
        
        logger.info("✅ Claude Sonnet 4 test completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Claude Sonnet 4 test failed: {e}")
        raise
