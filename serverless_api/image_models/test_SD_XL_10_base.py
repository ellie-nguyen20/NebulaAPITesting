import pytest
import requests
import logging

test_cases = [
    ("TC_00_CheckConnection", "A cat sitting on a beach", 200),
    ("TC_01_ValidRequest", "A futuristic cityscape with flying cars", 200),
    ("TC_02_LongPrompt", "A " * 5000, 200),
    ("TC_03_SpecialCharacters", "An astronaut riding a horse on Mars! 🚀🐎", 200),
    ("TC_04_EmptyPrompt", "", 400),
    ("TC_05_InvalidAPIKey", "A beautiful mountain view", 401),
    ("TC_06_NoAPIKey", "A sunset over the ocean", 401),
]

def build_headers(test_id, config):
    headers = {"Content-Type": "application/json"}
    if test_id == "TC_05_InvalidAPIKey":
        headers["Authorization"] = "Bearer INVALID_API_KEY"
    elif test_id != "TC_06_NoAPIKey":
        headers["Authorization"] = f"Bearer {config['api_key']}"
    return headers

def validate_response(test_id, result):
    assert "data" in result, f"{test_id}: Response missing 'data' field"
    assert isinstance(result["data"], list), f"{test_id}: 'data' is not a list"
    assert len(result["data"]) > 0, f"{test_id}: 'data' is empty"
    assert "b64_json" in result["data"][0], f"{test_id}: Missing 'b64_json' in first data item"

@pytest.mark.parametrize("test_id, prompt, expected_status", test_cases)
def test_nebula_sdxl_image_api(test_id, prompt, expected_status, config):
    headers = build_headers(test_id, config)

    payload = {
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "prompt": prompt,
        "num_steps": 4,
        "guidance_scale": 3.5,
        "seed": -1,
        "width": 1024,
        "height": 1024,
    }

    logging.info(f"Running {test_id} - Sending request to {config['image_base_url']}")

    response = requests.post(config['image_base_url'], headers=headers, json=payload, timeout=20)

    assert response.status_code == expected_status, f"{test_id}: Expected {expected_status}, got {response.status_code}"

    if response.status_code == 200:
        validate_response(test_id, response.json())
