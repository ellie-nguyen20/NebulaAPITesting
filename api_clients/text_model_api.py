from .base_model import BaseModel

class TextModelAPI(BaseModel):
    def __init__(self, base_model_url: str, api_key: str):
        super().__init__(base_model_url, api_key)

    def send_text_message(self, model: str, prompt: str, system_message: str = None):
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        }
        return self.send_request("chat/completions", "POST", data)