from api_clients.text_model_api import TextModelAPI

class TestMistralSmall(TextModelAPI):
    def __init__(self, model_api):
        super().__init__(model_api)

    def test_mistral_small(self):
        self.model_api.send_text_message(
            model="mistral-small",
            prompt="Hello, how are you?",
        )