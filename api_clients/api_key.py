from .base_api import BaseAPIClient

class APIKeyAPI(BaseAPIClient):
    """API Key API client for managing API key operations."""

    def get_api_keys(self):
        """Get all API keys."""
        return self.get("/keys")
    
    def create_new_api_key(self, name: str, description: str = "", team_id: int = None):
        """Create a new API key (personal or team)."""
        payload = {"name": name, "description": description}
        if team_id:
            payload["team_id"] = team_id
        return self.post("/keys", data=payload)

    def regenerate_api_key(self, api_key_id: str, name: str = None):
        """Regenerate an API key."""
        payload = {"regenerate": True}
        if name:
            payload["name"] = name
        return self.put(f"/keys/{api_key_id}", data=payload)
    
    def delete_api_key(self, api_key_id: str):
        """Delete an API key."""
        return self.delete(f"/keys/{api_key_id}")
    
  
    
