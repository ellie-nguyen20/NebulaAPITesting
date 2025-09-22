import pytest
import logging
from api_clients.image_api import ImageAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_bytedance_seedream_3_0_basic(config, api_key_scope_session):
    """Test Bytedance-Seedream-3.0 model - Basic functionality"""
    # Initialize image API
    image_config = {
        "image_generation_url": config["image_generation_url"],
        "api_key": api_key_scope_session
    }
    image_api = ImageAPI(image_config)
    
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

def test_flux_1_kontext_dev_basic(config, api_key_scope_session):
    """Test FLUX.1 [Kontext-dev] model - Basic functionality"""
    # Initialize image API
    image_config = {
        "image_generation_url": config["image_generation_url"],
        "api_key": api_key_scope_session
    }
    image_api = ImageAPI(image_config)
    
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

def test_image_generation_with_style(config, api_key_scope_session):
    """Test image generation with different styles"""
    # Initialize image API
    image_config = {
        "image_generation_url": config["image_generation_url"],
        "api_key": api_key_scope_session
    }
    image_api = ImageAPI(image_config)
    
    # Test different styles
    styles = ["realistic", "artistic", "cartoon", "anime"]
    base_prompt = "A cat sitting on a beach"
    
    print(f"\nTesting image generation with different styles...")
    print(f" Base prompt: {base_prompt}")
    
    for style in styles:
        print(f" Testing style: {style}")
        
        # Generate image with style
        response = image_api.generate_image_with_style("bytedance-seedream-3.0", base_prompt, style=style)
        
        # Validate response
        assert response.ok, f"Image generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert len(data["data"]) > 0, "'data' is empty"
        
        print(f"✅ Style '{style}' test completed successfully")
    
    print(f"✅ All style tests completed successfully")

def test_image_generation_multiple_images(config, api_key_scope_session):
    """Test generating multiple images from the same prompt"""
    # Initialize image API
    image_config = {
        "image_generation_url": config["image_generation_url"],
        "api_key": api_key_scope_session
    }
    image_api = ImageAPI(image_config)
    
    # Test data
    prompt = "A beautiful sunset over the ocean"
    num_images = 2
    
    print(f"\nTesting multiple image generation...")
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
        assert isinstance(image_data["b64_json"], str), f"'b64_json' should be a string in image {i+1}"
        assert len(image_data["b64_json"]) > 0, f"'b64_json' should not be empty in image {i+1}"
        print(f" Image {i+1} size: {len(image_data['b64_json'])} characters")
    
    print(f"✅ Multiple image generation test completed successfully")

def test_image_generation_with_dimensions(config, api_key_scope_session):
    """Test image generation with specific dimensions"""
    # Initialize image API
    image_config = {
        "image_generation_url": config["image_generation_url"],
        "api_key": api_key_scope_session
    }
    image_api = ImageAPI(image_config)
    
    # Test different dimensions
    dimensions = [(512, 512), (1024, 1024), (1024, 768)]
    prompt = "A futuristic robot in a laboratory"
    
    print(f"\nTesting image generation with different dimensions...")
    print(f" Prompt: {prompt}")
    
    for width, height in dimensions:
        print(f" Testing dimensions: {width}x{height}")
        
        # Generate image with specific dimensions
        response = image_api.generate_image_with_dimensions("bytedance-seedream-3.0", prompt, width=width, height=height)
        
        # Validate response
        assert response.ok, f"Image generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert len(data["data"]) > 0, "'data' is empty"
        
        print(f"✅ Dimensions {width}x{height} test completed successfully")
    
    print(f"✅ All dimension tests completed successfully")

def test_image_editing_with_flux_kontext_dev(config, api_key_scope_session):
    """Test image editing with FLUX.1 [Kontext-dev] model"""
    # Initialize image API
    image_config = {
        "image_generation_url": config["image_generation_url"],
        "api_key": api_key_scope_session
    }
    image_api = ImageAPI(image_config)
    
    # Test data
    prompt = "Add a hat to the cat"
    image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/cat.png"
    
    print(f"\nTesting image editing with FLUX.1 [Kontext-dev]...")
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
    
    print(f"✅ Image editing test completed successfully")
    print(f" Edited image size: {len(image_data['b64_json'])} characters")
