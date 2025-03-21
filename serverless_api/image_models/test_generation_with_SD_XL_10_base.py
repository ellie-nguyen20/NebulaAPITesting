from serverless_api.base_test import NEBULA_API_KEY, IMAGE_API_URL, test_results
import requests
import pytest
import logging


test_cases = [
    ("TC_00_CheckConnection", "A cat sitting on a beach", 200),
    ("TC_01_ValidRequest", "A futuristic cityscape with flying cars", 200),
    ("TC_02_LongPrompt", "A " * 5000, 200),
    ("TC_03_SpecialCharacters", "An astronaut riding a horse on Mars! 🚀🐎", 200),
    ("TC_04_EmptyPrompt", "", 200),
    ("TC_05_InvalidAPIKey", "A beautiful mountain view", 401),
    ("TC_06_NoAPIKey", "A sunset over the ocean", 401),
]


@pytest.mark.parametrize("test_id, prompt, expected_status", test_cases)
def test_nebula_image_api(test_id, prompt, expected_status):
    headers = {"Content-Type": "application/json"}

    if test_id == "TC_05_InvalidAPIKey":
        headers["Authorization"] = "Bearer INVALID_KEY"
    elif test_id != "TC_06_NoAPIKey":
        headers["Authorization"] = f"Bearer {NEBULA_API_KEY}"

    data = {
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "prompt": prompt,
        "num_steps": 25,
        "guidance_scale": 9,
        "negative_prompt": None,
        "width": 1024,
        "height": 1024,
    }

    logging.info(f"Running {test_id} - Sending request to {IMAGE_API_URL}")

    try:
        response = requests.post(IMAGE_API_URL, headers=headers, json=data, timeout=20)

        if response.status_code != expected_status:
            pytest.fail(
                f"{test_id} ❌ Failed! Expected {expected_status}, got {response.status_code}"
            )

        if response.status_code == 200:
            result = response.json()
            missing_fields = []

            if "data" not in result:
                missing_fields.append("'data' field")
            elif not isinstance(result["data"], list) or not result["data"]:
                missing_fields.append("'data' field is empty")
            elif "b64_json" not in result["data"][0]:
                missing_fields.append("'b64_json' field")

            if missing_fields:
                pytest.fail(
                    f"{test_id} ❌ Failed! Response missing: {', '.join(missing_fields)}"
                )

        logging.info(f"{test_id} ✅ Passed!")
        test_results.append((test_id, "✅ Passed", "-"))

    except Exception as e:
        pytest.fail(f"{test_id} ❌ Failed! Unexpected error: {e}", pytrace=True)
