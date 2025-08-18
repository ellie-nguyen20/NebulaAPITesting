# api_clients/api_key.py
"""
Simple API client for managing API keys through Nebula Block API endpoints.
Supports the 4 basic CRUD operations for API keys.
"""

from .base_api import BaseAPIClient
from typing import Dict, Any, List, Optional

class APIKeyAPI(BaseAPIClient):
    """
    Simple API client for managing API keys.
    Supports the 4 basic endpoints: GET, POST, PUT, DELETE.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        """
        Initialize the API Key API client.
        
        Args:
            base_url: Base URL for the Nebula Block API
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        super().__init__(base_url, api_key, timeout)
    
    def get_api_keys(self) -> Dict[str, Any]:
        """
        GET /api/v1/keys - Get all API keys.
        
        Returns:
            Dictionary containing API keys information
        """
        try:
            response = self.get("keys")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def generate_new_api_key(self, name: str, description: str = None, permissions: List[str] = None) -> Dict[str, Any]:
        """
        POST /api/v1/keys - Generate a new API key.
        
        Args:
            name: Name for the new API key
            description: Optional description
            permissions: List of permissions for the key
            
        Returns:
            Dictionary containing the new API key information
        """
        payload = {"name": name}
        
        if description:
            payload["description"] = description
        
        if permissions:
            payload["permissions"] = permissions
        
        try:
            response = self.post("keys", data=payload)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def update_api_key(self, key_id: str, name: str = None, description: str = None, 
                      permissions: List[str] = None, is_active: bool = None) -> Dict[str, Any]:
        """
        PUT /api/v1/keys/{key_id} - Update an existing API key.
        
        Args:
            key_id: ID of the API key to update
            name: New name for the key
            description: New description
            permissions: New list of permissions
            is_active: Whether the key should be active
            
        Returns:
            Dictionary containing the updated API key information
        """
        payload = {}
        
        if name is not None:
            payload["name"] = name
        
        if description is not None:
            payload["description"] = description
        
        if permissions is not None:
            payload["permissions"] = permissions
        
        if is_active is not None:
            payload["is_active"] = is_active
        
        try:
            response = self.put(f"keys/{key_id}", data=payload)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def delete_api_key(self, key_id: str) -> Dict[str, Any]:
        """
        DELETE /api/v1/keys/{key_id} - Delete an API key.
        
        Args:
            key_id: ID of the API key to delete
            
        Returns:
            Dictionary with success/error information
        """
        try:
            response = self.delete(f"keys/{key_id}")
            return {"success": True, "message": f"API key {key_id} deleted successfully"}
        except Exception as e:
            return {"error": str(e)}

# Convenience functions for easy use
def get_api_keys(base_url: str, api_key: str) -> Dict[str, Any]:
    """Get all API keys."""
    client = APIKeyAPI(base_url, api_key)
    return client.get_api_keys()

def generate_new_api_key(base_url: str, api_key: str, name: str, description: str = None, permissions: List[str] = None) -> Dict[str, Any]:
    """Create a new API key."""
    client = APIKeyAPI(base_url, api_key)
    return client.generate_new_api_key(name, description, permissions)

def update_api_key(base_url: str, api_key: str, key_id: str, **kwargs) -> Dict[str, Any]:
    """Update an API key."""
    client = APIKeyAPI(base_url, api_key)
    return client.update_api_key(key_id, **kwargs)

def delete_api_key(base_url: str, api_key: str, key_id: str) -> Dict[str, Any]:
    """Delete an API key."""
    client = APIKeyAPI(base_url, api_key)
    return client.delete_api_key(key_id)
