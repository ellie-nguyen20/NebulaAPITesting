from serverless_api.base_test import NEBULA_API_KEY, IMAGE_API_URL, test_results
import requests
import pytest
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

@pytest.mark.parametrize("test_id, prompt, expected_status", test_cases)
def test_nebula_flux_image_api(test_id, prompt, expected_status):
    """Test API generate image với model FLUX.1-schnell"""
    headers = {"Content-Type": "application/json"}

    if test_id not in ["TC_05_InvalidAPIKey", "TC_06_NoAPIKey"]:
        headers["Authorization"] = f"Bearer {NEBULA_API_KEY}"

    data = {
        "model_name": "black-forest-labs/FLUX.1-schnell",
        "prompt": prompt,
        "num_steps": 4,
        "guidance_scale": 3.5,
        "seed": -1,
        "width": 1024,
        "height": 1024
    }

    logging.info(f"Running {test_id}...")
    try:
        response = requests.post(IMAGE_API_URL, headers=headers, json=data, timeout=20)
        response.raise_for_status()

        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

        if response.status_code == 200:
            result = response.json()
            assert "image_url" in result, "Response missing 'image_url' field."

        logging.info(f"{test_id} ✅ Passed!")
        test_results.append((test_id, "✅ Passed", "-"))

    except Exception as e:
        logging.error(f"{test_id} ❌ Failed! Error: {str(e)}")
        test_results.append((test_id, "❌ Failed", str(e)))
