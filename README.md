# Nebula Block SDK Samples

## Overview
This repository contains sample code and tests for Nebula Block SDK. The project includes API tests for various models under the `serverless_api` directory.

## Prerequisites
Before running the tests, ensure you have the following installed:

- Python 3.x
- `pip`
- Virtual environment (recommended)

## Installation
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd nebula-block-sdk-samples
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate.bat  # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration
1. Create a `.env` file in the root directory with your API keys:
   ```
   NEBULA_API_KEY=your_api_key_here
   ```

2. The `config.yaml` file contains environment-specific configurations:
   ```yaml
   staging:
     base_url: https://staging-api-url
   production:
     base_url: https://production-api-url
   ```

## Running Tests

### Environment Selection


### Run all tests and Environment Selection
To run all test cases under `serverless_api` and generate an HTML report:
   ```sh
   pytest --html=report.html --self-contained-html # Staging and personal api key
   pytest --key=team --html=report.html --self-contained-html # Staging and team api key
   pytest --env=production --key=personal --html=report.html --self-contained-html # Production and personal api key
   pytest --env=production --key=team --html=report.html --self-contained-html # Production and team api key
   ```

### Run tests for a specific subdirectory
You can run tests inside a specific subdirectory, e.g., `vision_models`:
   ```sh
   pytest serverless_api/vision_models
   ```

### Run a specific test file
To run a single test file, specify its path:
   ```sh
   pytest serverless_api/vision_models/test_analysis_image_with_Qwen25_VL_7B_Instruct.py
   ```

## Viewing the Report
After running the tests, open `report.html` in a browser to see the test results.



