import requests
import pytest
import logging
from serverless_api.base_test import NEBULA_API_KEY, TEXT_API_URL, test_results


test_cases = [
    ("TC_00_ValidRequest", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
     "What is this image?", 200),
    ("TC_01_InvalidImageURL", "https://invalid-url.com/fake.jpg", "Describe this image.", 400),
    ("TC_02_NoImage", None, "What is in this image?", 400),
    (
    "TC_03_NoAPIKey", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg", "What is this?", 401),
    ("TC_04_EmptyText", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg", "", 200),
    ("TC_05_LongText", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg", "A" * 5000, 200),
    ("TC_06_SpecialCharacters", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg", "🔥💡🚀✨🎨",
     200),
    ("TC_07_HTMLInjection", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
     "<script>alert('Hacked!')</script>", 200),
    ("TC_08_SQLInjection", "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg", "' OR 1=1; --",
     200),
    ("TC_09_LargeImage", "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png",
     "What is in this image?", 200),
    ("TC_10_UnsupportedFormat", "https://media.giphy.com/media/3o7aD2saDZ99d0l3iY/giphy.gif", "Describe this image",
     400),
]


@pytest.mark.parametrize("test_id, image_url, text, expected_status", test_cases)
def test_vision_model(test_id, image_url, text, expected_status):
    """Test API Vision Model với nhiều tình huống khác nhau"""
    headers = {"Content-Type": "application/json"}

    # Nếu không phải test case "No API Key", thêm header Authorization
    if test_id != "TC_03_NoAPIKey":
        headers["Authorization"] = f"Bearer {NEBULA_API_KEY}"

    # Chuẩn bị payload request
    messages = [{"role": "user", "content": []}]

    if image_url:
        messages[0]["content"].append({"type": "image_url", "image_url": {"url": image_url}})

    messages[0]["content"].append({"type": "text", "text": text})

    data = {
        "messages": messages,
        "model": "Qwen/Qwen2.5-VL-7B-Instruct",
        "max_tokens": None,
        "temperature": 1,
        "top_p": 0.9,
        "stream": False
    }

    logging.info(f"Running {test_id}...")

    try:
        response = requests.post(VISION_API_URL, headers=headers, json=data, timeout=20)
        response.raise_for_status()

        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

        # Nếu là request hợp lệ, kiểm tra response format
        if response.status_code == 200:
            result = response.json()
            assert "choices" in result, "Response is missing 'choices' key"
            assert len(result["choices"]) > 0, "Empty response from model"
            assert "message" in result["choices"][0], "Missing 'message' in response"
            assert "content" in result["choices"][0]["message"], "Missing 'content' in response"

        logging.info(f"{test_id} ✅ Passed!")
        test_results.append((test_id, "✅ Passed", "-"))

    except Exception as e:
        logging.error(f"{test_id} ❌ Failed! Error: {str(e)}")
        test_results.append((test_id, "❌ Failed", str(e)))
