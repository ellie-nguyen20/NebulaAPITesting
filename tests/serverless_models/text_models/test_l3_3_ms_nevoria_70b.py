import pytest
import logging
from api_clients.text_models import TextModelsAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_l3_3_ms_nevoria_70b_simple(config_with_api_key):
    logger.info("🚀 Starting L3.3-MS-Nevoria-70b text test with simple prompt")
    
    try:
        text_api = TextModelsAPI(config_with_api_key)
        logger.info("✅ TextModelsAPI instance created successfully")
        
        response = text_api.call_model(
            model_name="l3.3-ms-nevoria-70b",
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
        logger.info(f"📝 L3.3-MS-Nevoria-70b text response: {content}")
        
        assert len(content) > 0, "Response content should not be empty"
        assert isinstance(content, str), "Response content should be a string"
        
        logger.info("✅ L3.3-MS-Nevoria-70b text test completed successfully")
        
    except Exception as e:
        logger.error(f"❌ L3.3-MS-Nevoria-70b text test failed: {e}")
        raise
