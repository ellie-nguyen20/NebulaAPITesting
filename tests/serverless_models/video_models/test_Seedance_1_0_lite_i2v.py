import pytest
import logging
from api_clients.video_api import VideoAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_seedance_1_0_lite_i2v_basic(config, api_key_scope_session):
    """Test Seedance-1-0-lite-i2v model - Basic functionality"""
    logger.info("🚀 Starting Seedance-1-0-lite-i2v video test with basic prompt")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        logger.info("✅ VideoAPI instance created successfully")
        
        # Test data
        prompt = "A beautiful sunset over the ocean with gentle waves"
        image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
        
        print(f"\nTesting Seedance-1-0-lite-i2v model...")
        print(f" Prompt: {prompt}")
        print(f" Image URI: {image_uri}")
        
        # Generate video from image
        response = video_api.generate_video_from_image("seedance-1-0-lite-i2v", prompt, image_uri=image_uri)
        
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
        
        print(f"✅ Seedance-1-0-lite-i2v test completed successfully")
        print(f" Generated video URL: {video_output}")
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-lite-i2v test failed: {e}")
        raise

def test_seedance_1_0_lite_i2v_with_aspect_ratio(config, api_key_scope_session):
    """Test Seedance-1-0-lite-i2v model with custom aspect ratio"""
    logger.info("🚀 Starting Seedance-1-0-lite-i2v video test with custom aspect ratio")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        
        # Test data
        prompt = "A forest with sunlight filtering through trees"
        image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
        aspect_ratio = "16:9"
        
        print(f"\nTesting Seedance-1-0-lite-i2v with aspect ratio {aspect_ratio}...")
        print(f" Prompt: {prompt}")
        print(f" Image URI: {image_uri}")
        
        # Generate video with custom aspect ratio
        response = video_api.generate_video_with_aspect_ratio("seedance-1-0-lite-i2v", prompt, aspect_ratio=aspect_ratio, image_uri=image_uri)
        
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
        
        print(f"✅ Seedance-1-0-lite-i2v aspect ratio test completed successfully")
        print(f" Generated video URL: {video_output}")
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-lite-i2v aspect ratio test failed: {e}")
        raise

def test_seedance_1_0_lite_i2v_with_camera_movement(config, api_key_scope_session):
    """Test Seedance-1-0-lite-i2v model with camera movement"""
    logger.info("🚀 Starting Seedance-1-0-lite-i2v video test with camera movement")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        
        # Test data
        prompt = "A drone flying over a mountain range with smooth camera movement"
        image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
        
        print(f"\nTesting Seedance-1-0-lite-i2v with camera movement...")
        print(f" Prompt: {prompt}")
        print(f" Image URI: {image_uri}")
        
        # Generate video with camera movement (camera_fixed=False)
        response = video_api.generate_video_from_image(
            "seedance-1-0-lite-i2v", 
            prompt, 
            image_uri=image_uri,
            camera_fixed=False,
            duration=4,
            fps=2
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
        
        print(f"✅ Seedance-1-0-lite-i2v camera movement test completed successfully")
        print(f" Generated video URL: {video_output}")
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-lite-i2v camera movement test failed: {e}")
        raise
