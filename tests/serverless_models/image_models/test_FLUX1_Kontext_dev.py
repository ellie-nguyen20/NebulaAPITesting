import pytest
import logging
from api_clients.image_api import ImageAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_flux_1_kontext_dev_basic(config, api_key_scope_session):
    """Test FLUX.1 [Kontext-dev] model - Basic functionality"""
    logger.info("🚀 Starting FLUX.1 [Kontext-dev] image test with basic prompt")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        logger.info("✅ ImageAPI instance created successfully")
        
        # Test data
        prompt = "A cyberpunk city with neon lights and rain"
        image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/cat.png"
        
        print(f"\nTesting FLUX.1 [Kontext-dev] model...")
        print(f" Prompt: {prompt}")
        print(f" Image URL: {image_url}")
        
        # Generate image (FLUX.1-Kontext-dev requires image parameter)
        response = image_api.edit_image("flux-1-kontext-dev", prompt, image_url)
        
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
        
        print(f"✅ FLUX.1 [Kontext-dev] test completed successfully")
        print(f" Generated image size: {len(image_data['b64_json'])} characters")
        
    except Exception as e:
        logger.error(f"❌ FLUX.1 [Kontext-dev] test failed: {e}")
        raise

def test_flux_1_kontext_dev_with_style(config, api_key_scope_session):
    """Test FLUX.1 [Kontext-dev] model with anime style"""
    logger.info("🚀 Starting FLUX.1 [Kontext-dev] image test with anime style")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        
        # Test data
        prompt = "A magical girl with sparkling eyes and flowing hair"
        style = "anime"
        image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/cat.png"
        
        print(f"\nTesting FLUX.1 [Kontext-dev] with {style} style...")
        print(f" Prompt: {prompt}")
        print(f" Image URL: {image_url}")
        
        # Generate image with style (FLUX.1-Kontext-dev requires image parameter)
        enhanced_prompt = f"{style} style: {prompt}"
        response = image_api.edit_image("flux-1-kontext-dev", enhanced_prompt, image_url)
        
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
        
        print(f"✅ FLUX.1 [Kontext-dev] {style} style test completed successfully")
        print(f" Generated image size: {len(image_data['b64_json'])} characters")
        
    except Exception as e:
        logger.error(f"❌ FLUX.1 [Kontext-dev] {style} style test failed: {e}")
        raise

def test_flux_1_kontext_dev_with_dimensions(config, api_key_scope_session):
    """Test FLUX.1 [Kontext-dev] model with specific dimensions"""
    logger.info("🚀 Starting FLUX.1 [Kontext-dev] image test with specific dimensions")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        
        # Test data
        prompt = "A futuristic space station orbiting a distant planet"
        width, height = 1024, 1024
        image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/cat.png"
        
        print(f"\nTesting FLUX.1 [Kontext-dev] with dimensions {width}x{height}...")
        print(f" Prompt: {prompt}")
        print(f" Image URL: {image_url}")
        
        # Generate image with specific dimensions (FLUX.1-Kontext-dev requires image parameter)
        response = image_api.edit_image("flux-1-kontext-dev", prompt, image_url, width=width, height=height)
        
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
        
        print(f"✅ FLUX.1 [Kontext-dev] dimensions {width}x{height} test completed successfully")
        print(f" Generated image size: {len(image_data['b64_json'])} characters")
        
    except Exception as e:
        logger.error(f"❌ FLUX.1 [Kontext-dev] dimensions test failed: {e}")
        raise

def test_flux_1_kontext_dev_edit_image(config, api_key_scope_session):
    """Test FLUX.1 [Kontext-dev] model for image editing"""
    logger.info("🚀 Starting FLUX.1 [Kontext-dev] image editing test")
    
    try:
        # Initialize image API
        image_config = {
            "image_generation_url": config["image_generation_url"],
            "api_key": api_key_scope_session
        }
        image_api = ImageAPI(image_config)
        
        # Test data
        prompt = "Add a hat to the cat"
        image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/cat.png"
        
        print(f"\nTesting FLUX.1 [Kontext-dev] image editing...")
        print(f" Prompt: {prompt}")
        print(f" Image URL: {image_url}")
        
        # Edit image
        response = image_api.edit_image("flux-1-kontext-dev", prompt, image_url)
        
        # Validate response
        assert response.ok, f"Image editing failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert len(data["data"]) > 0, "'data' is empty"
        
        # Validate image data
        image_data = data["data"][0]
        assert "b64_json" in image_data, "Missing 'b64_json' in image data"
        assert len(image_data["b64_json"]) > 0, "'b64_json' should not be empty"
        
        print(f"✅ FLUX.1 [Kontext-dev] image editing test completed successfully")
        print(f" Edited image size: {len(image_data['b64_json'])} characters")
        
    except Exception as e:
        logger.error(f"❌ FLUX.1 [Kontext-dev] image editing test failed: {e}")
        raise
