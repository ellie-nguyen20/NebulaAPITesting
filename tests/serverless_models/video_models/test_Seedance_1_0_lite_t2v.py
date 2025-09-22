import pytest
import logging
from api_clients.video_api import VideoAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_seedance_1_0_lite_t2v_basic(config, api_key_scope_session):
    """Test Seedance-1-0-lite-t2v model - Basic functionality"""
    logger.info("🚀 Starting Seedance-1-0-lite-t2v video test with basic prompt")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        logger.info("✅ VideoAPI instance created successfully")
        
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
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-lite-t2v test failed: {e}")
        raise

def test_seedance_1_0_lite_t2v_with_duration(config, api_key_scope_session):
    """Test Seedance-1-0-lite-t2v model with custom duration"""
    logger.info("🚀 Starting Seedance-1-0-lite-t2v video test with custom duration")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        
        # Test data
        prompt = "A waterfall cascading down rocks in a forest"
        duration = 6
        
        print(f"\nTesting Seedance-1-0-lite-t2v with duration {duration}s...")
        print(f" Prompt: {prompt}")
        
        # Generate video with custom duration
        response = video_api.generate_video_with_duration("seedance-1-0-lite-t2v", prompt, duration=duration)
        
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
        
        print(f"✅ Seedance-1-0-lite-t2v duration test completed successfully")
        print(f" Generated video URL: {video_output}")
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-lite-t2v duration test failed: {e}")
        raise

def test_seedance_1_0_lite_t2v_with_resolution(config, api_key_scope_session):
    """Test Seedance-1-0-lite-t2v model with custom resolution"""
    logger.info("🚀 Starting Seedance-1-0-lite-t2v video test with custom resolution")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        
        # Test data
        prompt = "A space station orbiting Earth with stars in the background"
        resolution = "720p"
        
        print(f"\nTesting Seedance-1-0-lite-t2v with resolution {resolution}...")
        print(f" Prompt: {prompt}")
        
        # Generate video with custom resolution
        response = video_api.generate_video_with_resolution("seedance-1-0-lite-t2v", prompt, resolution=resolution)
        
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
        
        print(f"✅ Seedance-1-0-lite-t2v resolution test completed successfully")
        print(f" Generated video URL: {video_output}")
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-lite-t2v resolution test failed: {e}")
        raise

def test_seedance_1_0_lite_t2v_with_aspect_ratio(config, api_key_scope_session):
    """Test Seedance-1-0-lite-t2v model with custom aspect ratio"""
    logger.info("🚀 Starting Seedance-1-0-lite-t2v video test with custom aspect ratio")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        
        # Test data
        prompt = "A tall building with clouds moving around it"
        aspect_ratio = "adaptive"
        
        print(f"\nTesting Seedance-1-0-lite-t2v with aspect ratio {aspect_ratio}...")
        print(f" Prompt: {prompt}")
        
        # Generate video with custom aspect ratio
        response = video_api.generate_video_with_aspect_ratio("seedance-1-0-lite-t2v", prompt, aspect_ratio=aspect_ratio)
        
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
        
        print(f"✅ Seedance-1-0-lite-t2v aspect ratio test completed successfully")
        print(f" Generated video URL: {video_output}")
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-lite-t2v aspect ratio test failed: {e}")
        raise
