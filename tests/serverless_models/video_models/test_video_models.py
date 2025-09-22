import pytest
import logging
from api_clients.video_api import VideoAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_seedance_1_0_pro_basic(config, api_key_scope_session):
    """Test Seedance-1-0-pro model - Basic functionality"""
    # Initialize video API
    video_config = {
        "video_generation_url": config["video_generation_url"],
        "api_key": api_key_scope_session
    }
    video_api = VideoAPI(video_config)
    
    # Test data
    prompt = "A static shot. A soldier operates a device, and the camera focus gradually shifts to the soldier's face."
    first_frame_image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
    last_frame_image_uri = ""
    
    print(f"\nTesting Seedance-1-0-pro model...")
    print(f" Prompt: {prompt}")
    print(f" First Frame Image URI: {first_frame_image_uri}")
    print(f" Last Frame Image URI: {last_frame_image_uri}")
    
    # Generate video from image
    response = video_api.generate_video_from_image("seedance-1-0-pro", prompt, first_frame_image_uri, last_frame_image_uri)
    
    # Validate response
    assert response.ok, f"Video generation failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f" Response data keys: {list(data.keys())}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert isinstance(data["data"], dict), f"'data' is not a dict, got {type(data['data'])}"
    assert "output" in data["data"], "Missing 'output' field in data"
    
    # Validate video data
    video_output = data["data"]["output"]
    assert isinstance(video_output, str), "'output' should be a string"
    assert len(video_output) > 0, "'output' should not be empty"
    assert video_output.startswith("http"), "Output should be a valid URL"
    
    print(f"✅ Seedance-1-0-pro test completed successfully")
    print(f" Generated video URL: {video_output}")

def test_seedance_1_0_lite_i2v_basic(config, api_key_scope_session):
    """Test Seedance-1-0-lite-i2v model - Basic functionality"""
    # Initialize video API
    video_config = {
        "video_generation_url": config["video_generation_url"],
        "api_key": api_key_scope_session
    }
    video_api = VideoAPI(video_config)
    
    # Test data
    prompt = "A beautiful sunset over the ocean with gentle waves"
    first_frame_image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
    last_frame_image_uri = ""
    
    print(f"\nTesting Seedance-1-0-lite-i2v model...")
    print(f" Prompt: {prompt}")
    print(f" First Frame Image URI: {first_frame_image_uri}")
    print(f" Last Frame Image URI: {last_frame_image_uri}")
    
    # Generate video from image
    response = video_api.generate_video_from_image("seedance-1-0-lite-i2v", prompt, first_frame_image_uri, last_frame_image_uri)
    
    # Validate response
    assert response.ok, f"Video generation failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    data = response.json()
    assert "data" in data, "Response missing 'data' field"
    assert isinstance(data["data"], dict), f"'data' is not a dict, got {type(data['data'])}"
    assert "output" in data["data"], "Missing 'output' field in data"
    
    # Validate video data
    video_output = data["data"]["output"]
    assert isinstance(video_output, str), "'output' should be a string"
    assert len(video_output) > 0, "'output' should not be empty"
    assert video_output.startswith("http"), "Output should be a valid URL"
    
    print(f"✅ Seedance-1-0-lite-i2v test completed successfully")
    print(f" Generated video URL: {video_output}")

def test_seedance_1_0_lite_t2v_basic(config, api_key_scope_session):
    """Test Seedance-1-0-lite-t2v model - Basic functionality"""
    # Initialize video API
    video_config = {
        "video_generation_url": config["video_generation_url"],
        "api_key": api_key_scope_session
    }
    video_api = VideoAPI(video_config)
    
    # Test data
    prompt = "A cat playing with a ball of yarn in slow motion"
    
    print(f"\nTesting Seedance-1-0-lite-t2v model...")
    print(f" Prompt: {prompt}")
    
    # Generate video from text
    response = video_api.generate_video("seedance-1-0-lite-t2v", prompt)
    
    # Validate response
    assert response.ok, f"Video generation failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f" Response data keys: {list(data.keys())}")
        print(f" Response data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert isinstance(data["data"], dict), f"'data' is not a dict, got {type(data['data'])}"
    assert "output" in data["data"], "Missing 'output' field in data"
    
    # Validate video data
    video_output = data["data"]["output"]
    assert isinstance(video_output, str), "'output' should be a string"
    assert len(video_output) > 0, "'output' should not be empty"
    assert video_output.startswith("http"), "Output should be a valid URL"
    
    print(f"✅ Seedance-1-0-lite-t2v test completed successfully")
    print(f" Generated video URL: {video_output}")

def test_video_generation_with_custom_parameters(config, api_key_scope_session):
    """Test video generation with custom parameters"""
    # Initialize video API
    video_config = {
        "video_generation_url": config["video_generation_url"],
        "api_key": api_key_scope_session
    }
    video_api = VideoAPI(video_config)
    
    # Test data
    prompt = "A futuristic city with flying cars"
    first_frame_image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
    last_frame_image_uri = ""
    
    print(f"\nTesting video generation with custom parameters...")
    print(f" Prompt: {prompt}")
    print(f" First Frame Image URI: {first_frame_image_uri}")
    print(f" Last Frame Image URI: {last_frame_image_uri}")
    
    # Generate video with custom parameters
    response = video_api.generate_video_from_image(
        "seedance-1-0-pro", 
        prompt, 
        first_frame_image_uri,
        last_frame_image_uri,
        duration=3,
        resolution="720p",
        aspect_ratio="adaptive",
        fps=2,
        seed=0.5,
        camera_fixed=True
    )
    
    # Validate response
    assert response.ok, f"Video generation failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    data = response.json()
    assert "data" in data, "Response missing 'data' field"
    assert isinstance(data["data"], dict), f"'data' is not a dict, got {type(data['data'])}"
    assert "output" in data["data"], "Missing 'output' field in data"
    
    # Validate video data
    video_output = data["data"]["output"]
    assert isinstance(video_output, str), "'output' should be a string"
    assert len(video_output) > 0, "'output' should not be empty"
    assert video_output.startswith("http"), "Output should be a valid URL"
    
    print(f"✅ Custom parameters test completed successfully")
    print(f" Generated video URL: {video_output}")
