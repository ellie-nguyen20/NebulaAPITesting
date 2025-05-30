import requests
import pytest
import logging

test_cases = [
    (
        "TC_00_ValidRequest",
        "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        "What is this image?",
        200,
    ),
    (
        "TC_01_InvalidImageURL",
        "https://invalid-url.com/fake.jpg",
        "Describe this image.",
        500,
    ),
    ("TC_02_NoImage", None, "What is in this image?", 200),
    (
        "TC_04_EmptyText",
        "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        "",
        200,
    ),
    (
        "TC_05_LongText",
        "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        "A" * 5000,
        200,
    ),
    (
        "TC_06_NoAPIKey",
        "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        "What is this?",
        401,
    ),
    (
        "TC_07_SpecialCharacters",
        "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        "🔥💡🚀✨🎨",
        200,
    ),
    (
        "TC_08_LargeImage",
        "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png",
        "What is in this image?",
        200,
    ),
    (
        "TC_09_UnsupportedFormat",
        "https://www.example.com/document.pdf",
        "Describe this image",
        500,
    ),
]

def build_headers(test_id, config):
    headers = {"Content-Type": "application/json"}
    if test_id == "TC_05_InvalidAPIKey":
        headers["Authorization"] = "Bearer INVALID_API_KEY"
    elif test_id != "TC_06_NoAPIKey":
        headers["Authorization"] = f"Bearer {config['api_key']}"
    return headers

def validate_response(test_id, result):
    assert "choices" in result, f"{test_id}: Response missing 'choices' field"
    assert isinstance(result["choices"], list), f"{test_id}: 'choices' is not a list"
    assert len(result["choices"]) > 0, f"{test_id}: 'choices' is empty"
    assert "message" in result["choices"][0], f"{test_id}: Missing 'message' in first choice"
    assert "content" in result["choices"][0]["message"], f"{test_id}: Missing 'content' in message"

@pytest.mark.parametrize("test_id, image_url, text, expected_status", test_cases)
def test_vision_model(test_id, image_url, text, expected_status, config):
    headers = build_headers(test_id, config)

    messages = [{"role": "user", "content": []}]

    if image_url:
        messages[0]["content"].append(
            {"type": "image_url", "image_url": {"url": image_url}}
        )

    messages[0]["content"].append({"type": "text", "text": text})

    data = {
        "messages": messages,
        "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct",
        "max_tokens": None,
        "temperature": 1,
        "top_p": 0.9,
        "stream": False,
    }

    logging.info(f"Running {test_id} - Sending request to {config['base_url']}")

    response = requests.post(config['base_url'], headers=headers, json=data, timeout=20)

    assert response.status_code == expected_status, f"{test_id}: Expected {expected_status}, got {response.status_code}"

    if response.status_code == 200:
        validate_response(test_id, response.json())
