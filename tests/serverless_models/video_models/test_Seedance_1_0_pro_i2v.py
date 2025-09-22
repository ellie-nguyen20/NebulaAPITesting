import pytest
import logging
from api_clients.video_api import VideoAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_seedance_1_0_pro_i2v_basic(config, api_key_scope_session):
    """Test Seedance-1.0-pro-i2v model - Basic functionality"""
    logger.info("🚀 Starting Seedance-1.0-pro-i2v video test with basic prompt")
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)
        logger.info("✅ VideoAPI instance created successfully")

        # Test data
        prompt = "A static shot. A soldier operates a device, and the camera focus gradually shifts to the soldier's face."
        image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"

        print(f"\nTesting Seedance-1.0-pro-i2v model...")
        print(f" Prompt: {prompt}")
        print(f" Image URI: {image_uri}")

        # Generate video from image
        response = video_api.generate_video_from_image("seedance-1-0-pro-i2v", prompt, image_uri=image_uri)

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
        assert isinstance(data["data"], dict), "'data' is not a dict"
        assert "output" in data["data"], "Missing 'output' field in data"

        # Validate video output
        video_output = data["data"]["output"]
        assert isinstance(video_output, str), "'output' should be a string"
        assert video_output.startswith("http"), "Video output should be a URL"
        assert len(video_output) > 0, "Video output should not be empty"

        print(f"✅ Seedance-1.0-pro-i2v test completed successfully")
        print(f" Generated video URL: {video_output}")

    except Exception as e:
        logger.error(f"❌ Seedance-1.0-pro-i2v test failed: {e}")
        raise

def test_seedance_1_0_pro_i2v_resolution(config, api_key_scope_session):
    """Test Seedance-1.0-pro-i2v model - Resolution parameter"""
    logger.info("🚀 Starting Seedance-1.0-pro-i2v resolution test")
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)

        # Test data
        prompt = "A beautiful landscape with mountains and lakes"
        image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
        resolution = "1080p"

        print(f"\nTesting Seedance-1.0-pro-i2v with resolution {resolution}...")
        print(f" Prompt: {prompt}")
        print(f" Image URI: {image_uri}")

        # Generate video with specific resolution
        response = video_api.generate_video_from_image("seedance-1-0-pro-i2v", prompt, image_uri=image_uri, resolution=resolution)

        # Validate response
        assert response.ok, f"Video generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert isinstance(data["data"], dict), "'data' is not a dict"
        assert "output" in data["data"], "Missing 'output' field in data"

        # Validate video output
        video_output = data["data"]["output"]
        assert isinstance(video_output, str), "'output' should be a string"
        assert video_output.startswith("http"), "Video output should be a URL"

        print(f"✅ Seedance-1.0-pro-i2v resolution test completed successfully")
        print(f" Generated video URL: {video_output}")

    except Exception as e:
        logger.error(f"❌ Seedance-1.0-pro-i2v resolution test failed: {e}")
        raise

def test_seedance_1_0_pro_i2v_duration(config, api_key_scope_session):
    """Test Seedance-1.0-pro-i2v model - Duration parameter"""
    logger.info("🚀 Starting Seedance-1.0-pro-i2v duration test")
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)

        # Test data
        prompt = "A cat playing with a ball of yarn"
        image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
        duration = 10

        print(f"\nTesting Seedance-1.0-pro-i2v with duration {duration}s...")
        print(f" Prompt: {prompt}")
        print(f" Image URI: {image_uri}")

        # Generate video with specific duration
        response = video_api.generate_video_from_image("seedance-1-0-pro-i2v", prompt, image_uri=image_uri, duration=duration)

        # Validate response
        assert response.ok, f"Video generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert isinstance(data["data"], dict), "'data' is not a dict"
        assert "output" in data["data"], "Missing 'output' field in data"

        # Validate video output
        video_output = data["data"]["output"]
        assert isinstance(video_output, str), "'output' should be a string"
        assert video_output.startswith("http"), "Video output should be a URL"

        print(f"✅ Seedance-1.0-pro-i2v duration test completed successfully")
        print(f" Generated video URL: {video_output}")

    except Exception as e:
        logger.error(f"❌ Seedance-1.0-pro-i2v duration test failed: {e}")
        raise

def test_seedance_1_0_pro_i2v_aspect_ratio(config, api_key_scope_session):
    """Test Seedance-1.0-pro-i2v model - Aspect ratio parameter"""
    logger.info("🚀 Starting Seedance-1.0-pro-i2v aspect ratio test")
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)

        # Test data
        prompt = "A panoramic view of a city skyline"
        image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
        aspect_ratio = "21:9"

        print(f"\nTesting Seedance-1.0-pro-i2v with aspect ratio {aspect_ratio}...")
        print(f" Prompt: {prompt}")
        print(f" Image URI: {image_uri}")

        # Generate video with specific aspect ratio
        response = video_api.generate_video_from_image("seedance-1-0-pro-i2v", prompt, image_uri=image_uri, aspect_ratio=aspect_ratio)

        # Validate response
        assert response.ok, f"Video generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert isinstance(data["data"], dict), "'data' is not a dict"
        assert "output" in data["data"], "Missing 'output' field in data"

        # Validate video output
        video_output = data["data"]["output"]
        assert isinstance(video_output, str), "'output' should be a string"
        assert video_output.startswith("http"), "Video output should be a URL"

        print(f"✅ Seedance-1.0-pro-i2v aspect ratio test completed successfully")
        print(f" Generated video URL: {video_output}")

    except Exception as e:
        logger.error(f"❌ Seedance-1.0-pro-i2v aspect ratio test failed: {e}")
        raise

def test_seedance_1_0_pro_i2v_camera_movement(config, api_key_scope_session):
    """Test Seedance-1.0-pro-i2v model - Camera movement parameter"""
    logger.info("🚀 Starting Seedance-1.0-pro-i2v camera movement test")
    try:
        # Initialize video API
        video_config = {
            "video_generation_url": config["video_generation_url"],
            "api_key": api_key_scope_session
        }
        video_api = VideoAPI(video_config)

        # Test data
        prompt = "A dynamic shot with camera movement following the subject"
        image_uri = "https://ark-auto-3000600237-ap-southeast-1-default.tos-ap-southeast-1.bytepluses.com/experience_video_demo/experience_videowQ9qL8pY.jpg"
        camera_fixed = False

        print(f"\nTesting Seedance-1.0-pro-i2v with camera movement...")
        print(f" Prompt: {prompt}")
        print(f" Image URI: {image_uri}")
        print(f" Camera Fixed: {camera_fixed}")

        # Generate video with camera movement
        response = video_api.generate_video_from_image("seedance-1-0-pro-i2v", prompt, image_uri=image_uri, camera_fixed=camera_fixed)

        # Validate response
        assert response.ok, f"Video generation failed with status {response.status_code}"
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

        # Parse response data
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert isinstance(data["data"], dict), "'data' is not a dict"
        assert "output" in data["data"], "Missing 'output' field in data"

        # Validate video output
        video_output = data["data"]["output"]
        assert isinstance(video_output, str), "'output' should be a string"
        assert video_output.startswith("http"), "Video output should be a URL"

        print(f"✅ Seedance-1.0-pro-i2v camera movement test completed successfully")
        print(f" Generated video URL: {video_output}")

    except Exception as e:
        logger.error(f"❌ Seedance-1.0-pro-i2v camera movement test failed: {e}")
        raise
