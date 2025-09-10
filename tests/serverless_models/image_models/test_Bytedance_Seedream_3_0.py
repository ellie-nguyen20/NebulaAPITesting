import pytest
import logging
from api_clients.image_api import ImageAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_bytedance_seedream_3_0_basic(config, api_key_scope_session):
    """Test Bytedance-Seedream-3.0 model - Basic functionality"""
    logger.info("🚀 Starting Bytedance-Seedream-3.0 image test with basic prompt")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        logger.info("✅ ImageAPI instance created successfully")
        
        # Test data
        prompt = "A futuristic cityscape with flying cars and neon lights"
        
        print(f"\nTesting Bytedance-Seedream-3.0 model...")
        print(f" Prompt: {prompt}")
        
        # Generate image
        response = image_api.generate_image("bytedance-seedream-3.0", prompt)
        
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
        
        print(f"✅ Bytedance-Seedream-3.0 test completed successfully")
        print(f" Generated image size: {len(image_data['b64_json'])} characters")
        
    except Exception as e:
        logger.error(f"❌ Bytedance-Seedream-3.0 test failed: {e}")
        raise

def test_bytedance_seedream_3_0_with_style(config, api_key_scope_session):
    """Test Bytedance-Seedream-3.0 model with artistic style"""
    logger.info("🚀 Starting Bytedance-Seedream-3.0 image test with artistic style")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        
        # Test data
        prompt = "A majestic dragon soaring through clouds"
        style = "artistic"
        
        print(f"\nTesting Bytedance-Seedream-3.0 with {style} style...")
        print(f" Prompt: {prompt}")
        
        # Generate image with style
        response = image_api.generate_image_with_style("bytedance-seedream-3.0", prompt, style=style)
        
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
        
        print(f"✅ Bytedance-Seedream-3.0 {style} style test completed successfully")
        print(f" Generated image size: {len(image_data['b64_json'])} characters")
        
    except Exception as e:
        logger.error(f"❌ Bytedance-Seedream-3.0 {style} style test failed: {e}")
        raise

def test_bytedance_seedream_3_0_multiple_images(config, api_key_scope_session):
    """Test Bytedance-Seedream-3.0 model generating multiple images"""
    logger.info("🚀 Starting Bytedance-Seedream-3.0 multiple images test")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        
        # Test data
        prompt = "A beautiful sunset over the ocean"
        num_images = 2
        
        print(f"\nTesting Bytedance-Seedream-3.0 multiple images...")
        print(f" Prompt: {prompt}")
        print(f" Number of images: {num_images}")
        
        # Generate multiple images
        response = image_api.generate_multiple_images("bytedance-seedream-3.0", prompt, num_images=num_images)
        
        # Validate response
        assert response.ok, f"Image generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert isinstance(data["data"], list), "'data' is not a list"
        assert len(data["data"]) == num_images, f"Expected {num_images} images, got {len(data['data'])}"
        
        # Validate each image
        for i, image_data in enumerate(data["data"]):
            assert "b64_json" in image_data, f"Missing 'b64_json' in image {i+1}"
            assert len(image_data["b64_json"]) > 0, f"'b64_json' should not be empty in image {i+1}"
            print(f" Image {i+1} size: {len(image_data['b64_json'])} characters")
        
        print(f"✅ Bytedance-Seedream-3.0 multiple images test completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Bytedance-Seedream-3.0 multiple images test failed: {e}")
        raise
