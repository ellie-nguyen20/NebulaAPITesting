import pytest
import logging
from api_clients.image_api import ImageAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_sd_xl_1_0_base_basic(config, api_key_scope_session):
    """Test SD-XL 1.0-base model - Basic functionality"""
    logger.info("🚀 Starting SD-XL 1.0-base image test with basic prompt")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        logger.info("✅ ImageAPI instance created successfully")
        
        # Test data
        prompt = "A beautiful mountain landscape at sunset"
        
        print(f"\nTesting SD-XL 1.0-base model...")
        print(f" Prompt: {prompt}")
        
        # Generate image
        response = image_api.generate_image("sd-xl-1.0-base", prompt)
        
        # Validate response
        assert response.ok, f"Image generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        try:
            data = response.json()
            print(f" Response data keys: {list(data.keys())}")
        except Exception as e:
            pytest.fail(f"Failed to parse JSON response: {e}")
        
        # Validate response structure
        assert "data" in data, "Response missing 'data' field"
        assert isinstance(data["data"], list), "'data' is not a list"
        assert len(data["data"]) > 0, "'data' is empty"
        
        # Validate image data
        image_data = data["data"][0]
        assert "b64_json" in image_data, "Missing 'b64_json' in image data"
        assert isinstance(image_data["b64_json"], str), "'b64_json' should be a string"
        assert len(image_data["b64_json"]) > 0, "'b64_json' should not be empty"
        
        print(f"✅ SD-XL 1.0-base test completed successfully")
        print(f" Generated image size: {len(image_data['b64_json'])} characters")
        
    except Exception as e:
        logger.error(f"❌ SD-XL 1.0-base test failed: {e}")
        raise

def test_sd_xl_1_0_base_with_style(config, api_key_scope_session):
    """Test SD-XL 1.0-base model with realistic style"""
    logger.info("🚀 Starting SD-XL 1.0-base image test with realistic style")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        
        # Test data
        prompt = "A professional portrait of a business person"
        style = "realistic"
        
        print(f"\nTesting SD-XL 1.0-base with {style} style...")
        print(f" Prompt: {prompt}")
        
        # Generate image with style
        response = image_api.generate_image_with_style("sd-xl-1.0-base", prompt, style=style)
        
        # Validate response
        assert response.ok, f"Image generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert len(data["data"]) > 0, "'data' is empty"
        
        # Validate image data
        image_data = data["data"][0]
        assert "b64_json" in image_data, "Missing 'b64_json' in image data"
        assert len(image_data["b64_json"]) > 0, "'b64_json' should not be empty"
        
        print(f"✅ SD-XL 1.0-base {style} style test completed successfully")
        print(f" Generated image size: {len(image_data['b64_json'])} characters")
        
    except Exception as e:
        logger.error(f"❌ SD-XL 1.0-base {style} style test failed: {e}")
        raise

def test_sd_xl_1_0_base_with_dimensions(config, api_key_scope_session):
    """Test SD-XL 1.0-base model with specific dimensions"""
    logger.info("🚀 Starting SD-XL 1.0-base image test with specific dimensions")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        
        # Test data
        prompt = "A futuristic robot in a laboratory"
        width, height = 1024, 768
        
        print(f"\nTesting SD-XL 1.0-base with dimensions {width}x{height}...")
        print(f" Prompt: {prompt}")
        
        # Generate image with specific dimensions
        response = image_api.generate_image_with_dimensions("sd-xl-1.0-base", prompt, width=width, height=height)
        
        # Validate response
        assert response.ok, f"Image generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert len(data["data"]) > 0, "'data' is empty"
        
        # Validate image data
        image_data = data["data"][0]
        assert "b64_json" in image_data, "Missing 'b64_json' in image data"
        assert len(image_data["b64_json"]) > 0, "'b64_json' should not be empty"
        
        print(f"✅ SD-XL 1.0-base dimensions {width}x{height} test completed successfully")
        print(f" Generated image size: {len(image_data['b64_json'])} characters")
        
    except Exception as e:
        logger.error(f"❌ SD-XL 1.0-base dimensions test failed: {e}")
        raise
