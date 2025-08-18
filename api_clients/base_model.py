import requests

class BaseModel:
    def __init__(self, base_model_url: str, api_key: str):
        self.base_model_url = base_model_url
        self.api_key = api_key

    def send_request(self, endpoint: str, method: str, data: dict = None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.request(method, f"{self.base_model_url}/{endpoint}", headers=headers, json=data)
        return response.json()