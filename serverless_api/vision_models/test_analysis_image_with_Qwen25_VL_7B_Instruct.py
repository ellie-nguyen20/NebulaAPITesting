import requests
import pytest
import logging
from serverless_api.base_test import NEBULA_API_KEY, TEXT_API_URL, test_results

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
        "TC_03_NoAPIKey",
        "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        "What is this?",
        401,
    ),
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
        "TC_06_SpecialCharacters",
        "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        "🔥💡🚀✨🎨",
        200,
    ),
    (
        "TC_07_LargeImage",
        "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png",
        "What is in this image?",
        200,
    ),
    (
        "TC_08_UnsupportedFormat",
        "https://www.example.com/document.pdf",
        "Describe this image",
        500,
    ),
]


@pytest.mark.parametrize("test_id, image_url, text, expected_status", test_cases)
def test_vision_model(test_id, image_url, text, expected_status):
    headers = {"Content-Type": "application/json"}

    if test_id != "TC_03_NoAPIKey":
        headers["Authorization"] = f"Bearer {NEBULA_API_KEY}"

    messages = [{"role": "user", "content": []}]

    if image_url:
        messages[0]["content"].append(
            {"type": "image_url", "image_url": {"url": image_url}}
        )

    messages[0]["content"].append({"type": "text", "text": text})

    data = {
        "messages": messages,
        "model": "Qwen/Qwen2.5-VL-7B-Instruct",
        "max_tokens": None,
        "temperature": 1,
        "top_p": 0.9,
        "stream": False,
    }

    logging.info(f"Running {test_id} - Sending request to {TEXT_API_URL}")

    try:
        response = requests.post(TEXT_API_URL, headers=headers, json=data, timeout=20)

        if response.status_code != expected_status:
            pytest.fail(
                f"{test_id} ❌ Failed! Expected {expected_status}, got {response.status_code}"
            )

        if response.status_code == 200:
            result = response.json()
            missing_fields = []

            if "choices" not in result:
                missing_fields.append("'choices' key")
            elif not isinstance(result["choices"], list) or not result["choices"]:
                missing_fields.append("'choices' is empty")
            elif "message" not in result["choices"][0]:
                missing_fields.append("'message' in response")
            elif "content" not in result["choices"][0]["message"]:
                missing_fields.append("'content' in response")

            if missing_fields:
                pytest.fail(
                    f"{test_id} ❌ Failed! Response missing: {', '.join(missing_fields)}"
                )

        logging.info(f"{test_id} ✅ Passed!")
        test_results.append((test_id, "✅ Passed", "-"))

    except Exception as e:
        pytest.fail(f"{test_id} ❌ Failed! Unexpected error: {e}", pytrace=True)
