import pytest
import logging
from api_clients.video_api import VideoAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_seedance_1_0_pro_basic(config, api_key_scope_session):
    """Test Seedance-1-0-pro model - Basic functionality"""
    logger.info("🚀 Starting Seedance-1-0-pro video test with basic prompt")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        logger.info("✅ VideoAPI instance created successfully")
        
        # Test data
        prompt = "A superbike rider leans into a curve on a mountain road at night. The headlights cut through the darkness, leaving glowing light trails behind."
        
        print(f"\nTesting Seedance-1-0-pro model...")
        print(f" Prompt: {prompt}")
        
        # Generate video from text (text-to-video)
        response = video_api.generate_video("seedance-1-0-pro-t2v", prompt)
        
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
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-pro test failed: {e}")
        raise

def test_seedance_1_0_pro_with_duration(config, api_key_scope_session):
    """Test Seedance-1-0-pro model with custom duration"""
    logger.info("🚀 Starting Seedance-1-0-pro video test with custom duration")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        
        # Test data
        prompt = "A beautiful landscape with mountains and lakes"
        duration = 3
        
        print(f"\nTesting Seedance-1-0-pro with duration {duration}s...")
        print(f" Prompt: {prompt}")
        
        # Generate video with custom duration
        response = video_api.generate_video_with_duration("seedance-1-0-pro-t2v", prompt, duration=duration)
        
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
        
        print(f"✅ Seedance-1-0-pro duration test completed successfully")
        print(f" Generated video URL: {video_output}")
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-pro duration test failed: {e}")
        raise

def test_seedance_1_0_pro_with_resolution(config, api_key_scope_session):
    """Test Seedance-1-0-pro model with custom resolution"""
    logger.info("🚀 Starting Seedance-1-0-pro video test with custom resolution")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        
        # Test data
        prompt = "A city skyline at night with neon lights"
        resolution = "1080p"
        
        print(f"\nTesting Seedance-1-0-pro with resolution {resolution}...")
        print(f" Prompt: {prompt}")
        
        # Generate video with custom resolution
        response = video_api.generate_video_with_resolution("seedance-1-0-pro-t2v", prompt, resolution=resolution)
        
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
        
        print(f"✅ Seedance-1-0-pro resolution test completed successfully")
        print(f" Generated video URL: {video_output}")
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-pro resolution test failed: {e}")
        raise

def test_seedance_1_0_pro_text_to_video(config, api_key_scope_session):
    """Test Seedance-1-0-pro model - Text-to-Video generation (no image)"""
    logger.info("🚀 Starting Seedance-1-0-pro text-to-video test")
    
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        
        # Test data - using the exact prompt from your API example
        prompt = "A superbike rider leans into a curve on a mountain road at night. The headlights cut through the darkness, leaving glowing light trails behind."
        
        print(f"\nTesting Seedance-1-0-pro text-to-video generation...")
        print(f" Prompt: {prompt}")
        
        # Generate video from text only (no image)
        response = video_api.generate_video("seedance-1-0-pro-t2v", prompt)
        
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
        
        print(f"✅ Seedance-1-0-pro text-to-video test completed successfully")
        print(f" Generated video URL: {video_output}")
        
    except Exception as e:
        logger.error(f"❌ Seedance-1-0-pro text-to-video test failed: {e}")
        raise
