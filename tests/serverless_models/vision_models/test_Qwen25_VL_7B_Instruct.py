import pytest
import logging
from api_clients.vision_api import VisionAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_qwen25_vl_7b_instruct_basic(config, api_key_scope_session):
    """Test Qwen2.5-VL-7B-Instruct model - Basic functionality"""
    
    # Initialize vision API
    vision_config = {
        "chat_completions_url": config["chat_completions_url"],
        "api_key": api_key_scope_session
    }
    vision_api = VisionAPI(vision_config)
    
    # Test data
    image_url = "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"
    text = "What is this image?"
    
    print(f"\nTesting Qwen2.5-VL-7B-Instruct model...")
    print(f"  Image URL: {image_url}")
    print(f"  Text: {text}")
    
    # Chat with image
    response = vision_api.chat_with_image("qwen2.5-vl-7b-instruct", image_url, text)
    
    # Validate response
    assert response.ok, f"Vision chat failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f"  Response data keys: {list(data.keys())}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "choices" in data, "Response missing 'choices' field"
    assert "model" in data, "Response missing 'model' field"
    assert "usage" in data, "Response missing 'usage' field"
    
    # Validate choices field
    choices = data["choices"]
    assert isinstance(choices, list), "Choices should be a list"
    assert len(choices) > 0, "Should have at least one choice"
    
    # Validate first choice
    choice = choices[0]
    assert isinstance(choice, dict), "Choice should be a dictionary"
    assert "message" in choice, "Choice missing 'message' field"
    assert "finish_reason" in choice, "Choice missing 'finish_reason' field"
    
    # Validate message structure
    message = choice["message"]
    assert isinstance(message, dict), "Message should be a dictionary"
    assert "role" in message, "Message missing 'role' field"
    assert "content" in message, "Message missing 'content' field"
    
    # Validate content
    content = message["content"]
    assert isinstance(content, str), "Content should be a string"
    assert len(content) > 0, "Content should not be empty"
    
    # Validate model field
    assert data["model"] == "Qwen/Qwen2.5-VL-7B-Instruct", f"Expected model 'Qwen/Qwen2.5-VL-7B-Instruct', got '{data['model']}'"
    
    # Validate usage field
    usage = data["usage"]
    assert isinstance(usage, dict), "Usage should be a dictionary"
    assert "prompt_tokens" in usage, "Usage missing 'prompt_tokens' field"
    assert "completion_tokens" in usage, "Usage missing 'completion_tokens' field"
    assert "total_tokens" in usage, "Usage missing 'total_tokens' field"
    
    print(f"  Model: {data['model']}")
    print(f"  Response: {content[:100]}...")
    print(f"  Usage: {usage}")
    print(f"  Qwen2.5-VL-7B-Instruct test completed successfully!")

def test_qwen25_vl_7b_instruct_image_analysis(config, api_key_scope_session):
    """Test Qwen2.5-VL-7B-Instruct with different analysis types"""
    
    # Initialize vision API
    vision_config = {
        "chat_completions_url": config["chat_completions_url"],
        "api_key": api_key_scope_session
    }
    vision_api = VisionAPI(vision_config)
    
    # Test data
    image_url = "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"
    
    print(f"\nTesting Qwen2.5-VL-7B-Instruct image analysis...")
    print(f"  Image URL: {image_url}")
    
    # Test different analysis types
    analysis_types = ["general", "objects", "text", "colors", "emotions", "detailed"]
    
    for analysis_type in analysis_types:
        print(f"    Testing {analysis_type} analysis...")
        
        response = vision_api.analyze_image("qwen2.5-vl-7b-instruct", image_url, analysis_type)
        
        # Validate response
        assert response.ok, f"{analysis_type} analysis failed with status {response.status_code}"
        
        data = response.json()
        choices = data["choices"]
        assert len(choices) > 0, f"Should have at least one choice for {analysis_type} analysis"
        
        content = choices[0]["message"]["content"]
        assert len(content) > 0, f"Content should not be empty for {analysis_type} analysis"
        
        print(f"      {analysis_type}: {content[:50]}...")
    
    print(f"  Image analysis test completed successfully!")

def test_qwen25_vl_7b_instruct_performance(config, api_key_scope_session):
    """Test Qwen2.5-VL-7B-Instruct performance with multiple requests"""
    
    # Initialize vision API
    vision_config = {
        "chat_completions_url": config["chat_completions_url"],
        "api_key": api_key_scope_session
    }
    vision_api = VisionAPI(vision_config)
    
    # Test data
    image_url = "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"
    texts = [
        "What is this image?",
        "Describe the main objects in this image.",
        "What colors do you see?",
        "What is the mood of this image?",
        "Provide a detailed description."
    ]
    
    print(f"\nTesting Qwen2.5-VL-7B-Instruct performance...")
    print(f"  Image URL: {image_url}")
    print(f"  Text prompts: {len(texts)}")
    
    start_time = time.time()
    
    # Test each text prompt
    for i, text in enumerate(texts):
        print(f"    Request {i+1}: {text}")
        response = vision_api.chat_with_image("qwen2.5-vl-7b-instruct", image_url, text)
        assert response.ok, f"Request {i+1} failed with status {response.status_code}"
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"  Processing time: {duration:.2f} seconds")
    print(f"  Requests per second: {len(texts) / duration:.2f}")
    print(f"  Performance test completed successfully!")

def test_qwen25_vl_7b_instruct_different_images(config, api_key_scope_session):
    """Test Qwen2.5-VL-7B-Instruct with different images"""
    
    # Initialize vision API
    vision_config = {
        "chat_completions_url": config["chat_completions_url"],
        "api_key": api_key_scope_session
    }
    vision_api = VisionAPI(vision_config)
    
    # Test data with different image URLs
    image_urls = [
        "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Vd-Orig.png/256px-Vd-Orig.png"
    ]
    
    print(f"\nTesting Qwen2.5-VL-7B-Instruct with different images...")
    print(f"  Image URLs: {len(image_urls)}")
    
    for i, image_url in enumerate(image_urls):
        print(f"    Image {i+1}: {image_url}")
        
        response = vision_api.chat_with_image("qwen2.5-vl-7b-instruct", image_url, "What do you see in this image?")
        
        # Validate response
        assert response.ok, f"Image {i+1} failed with status {response.status_code}"
        
        data = response.json()
        choices = data["choices"]
        assert len(choices) > 0, f"Should have at least one choice for image {i+1}"
        
        content = choices[0]["message"]["content"]
        assert len(content) > 0, f"Content should not be empty for image {i+1}"
        
        print(f"      Response: {content[:50]}...")
    
    print(f"  Different images test completed successfully!")

def test_qwen25_vl_7b_instruct_batch_analysis(config, api_key_scope_session):
    """Test Qwen2.5-VL-7B-Instruct batch analysis"""
    
    # Initialize vision API
    vision_config = {
        "chat_completions_url": config["chat_completions_url"],
        "api_key": api_key_scope_session
    }
    vision_api = VisionAPI(vision_config)
    
    # Test data
    image_analysis_pairs = [
        {
            "image_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
            "text": "What is this image?"
        },
        {
            "image_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
            "text": "Describe the colors in this image."
        },
        {
            "image_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
            "text": "What objects can you identify?"
        }
    ]
    
    print(f"\nTesting Qwen2.5-VL-7B-Instruct batch analysis...")
    print(f"  Analysis pairs: {len(image_analysis_pairs)}")
    
    # Process batch
    responses = vision_api.batch_vision_analysis("qwen2.5-vl-7b-instruct", image_analysis_pairs)
    
    assert len(responses) == len(image_analysis_pairs), f"Expected {len(image_analysis_pairs)} responses, got {len(responses)}"
    
    for i, response in enumerate(responses):
        assert response.ok, f"Batch {i} failed with status {response.status_code}"
        
        data = response.json()
        choices = data["choices"]
        assert len(choices) > 0, f"Should have at least one choice for batch {i}"
        
        content = choices[0]["message"]["content"]
        print(f"    Batch {i+1}: {content[:50]}...")
    
    print(f"  Batch analysis test completed successfully!")

def test_qwen25_vl_7b_instruct_error_handling(config, api_key_scope_session):
    """Test Qwen2.5-VL-7B-Instruct error handling"""
    
    # Initialize vision API
    vision_config = {
        "chat_completions_url": config["chat_completions_url"],
        "api_key": api_key_scope_session
    }
    vision_api = VisionAPI(vision_config)
    
    print(f"\nTesting Qwen2.5-VL-7B-Instruct error handling...")
    
    # Test with invalid image URL
    print(f"  Testing invalid image URL...")
    response = vision_api.chat_with_image("qwen2.5-vl-7b-instruct", "https://invalid-url.com/nonexistent.jpg", "What is this image?")
    
    if response.ok:
        print(f"    Invalid image URL accepted (unexpected)")
    else:
        print(f"    Invalid image URL correctly rejected: {response.status_code}")
        assert response.status_code in [400, 404, 422], f"Expected 400/404/422 for invalid image URL, got {response.status_code}"
    
    # Test with empty text
    print(f"  Testing empty text...")
    response = vision_api.chat_with_image("qwen2.5-vl-7b-instruct", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg", "")
    
    if response.ok:
        print(f"    Empty text accepted (unexpected)")
    else:
        print(f"    Empty text correctly rejected: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected 400/422 for empty text, got {response.status_code}"
    
    print(f"  Error handling test completed successfully!")

def test_qwen25_vl_7b_instruct_edge_cases(config, api_key_scope_session):
    """Test Qwen2.5-VL-7B-Instruct with edge cases"""
    
    # Initialize vision API
    vision_config = {
        "chat_completions_url": config["chat_completions_url"],
        "api_key": api_key_scope_session
    }
    vision_api = VisionAPI(vision_config)
    
    print(f"\nTesting Qwen2.5-VL-7B-Instruct edge cases...")
    
    # Test with very long text
    print(f"  Testing long text prompt...")
    long_text = "Please provide a very detailed analysis of this image, including all the objects you can see, the colors present, the composition, the lighting, the mood, and any other relevant details you can observe. Be as thorough as possible in your description."
    
    response = vision_api.chat_with_image("qwen2.5-vl-7b-instruct", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg", long_text)
    assert response.ok, f"Long text failed with status {response.status_code}"
    
    # Test with very short text
    print(f"  Testing short text prompt...")
    response = vision_api.chat_with_image("qwen2.5-vl-7b-instruct", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg", "?")
    assert response.ok, f"Short text failed with status {response.status_code}"
    
    # Test with special characters in text
    print(f"  Testing special characters...")
    special_text = "What do you see? Please describe in detail! @#$%^&*()"
    response = vision_api.chat_with_image("qwen2.5-vl-7b-instruct", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg", special_text)
    assert response.ok, f"Special characters failed with status {response.status_code}"
    
    print(f"  Edge cases test completed successfully!")
