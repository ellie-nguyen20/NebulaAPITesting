from .base_api import BaseAPIClient

class APIKeyAPI(BaseAPIClient):
    """API Key API client for managing API key operations."""

    def get_api_keys(self):
        """Get all API keys."""
        return self.get("/keys")
    
    def generate_new_api_key(self, name: str):
        """Create a new API key."""
        payload = {"name": name}
        return self.post("/api_keys", data=payload)