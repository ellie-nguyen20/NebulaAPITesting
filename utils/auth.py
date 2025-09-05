"""
Authentication utilities for Nebula Block SDK
Handles API key management and authentication
"""

import os
import yaml
import requests
from typing import Dict, Any, Optional
# No longer using .env file - authentication is done through account login

class NebulaAuth:
    """Authentication class for Nebula Block API - Focused on API key management"""
    
    def __init__(self, environment: str = "staging", config_data: Optional[Dict[str, Any]] = None):
        """
        Initialize authentication with environment
        
        Args:
            environment (str): "staging" or "production"
            config_data (dict, optional): Pre-loaded config data from conftest.py
        """
        self.environment = environment
        
        # Use provided config or load from file
        if config_data:
            self.config = config_data
        else:
            self.config = self._load_config()
            
        self.api_key = self._get_api_key()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.yaml (fallback method)"""
        try:
            with open("config.yaml", "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
            return config
        except FileNotFoundError:
            raise FileNotFoundError("config.yaml not found")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config.yaml: {e}")
    
    def _get_api_key(self) -> str:
        """Get API key from environment variables"""
        # Try different environment variable patterns
        env_vars = [
            f"{self.environment.upper()}_PERSONAL_KEY",
            f"{self.environment.upper()}_TEAM_KEY", 
            "NEBULA_API_KEY",
            "API_KEY"
        ]
        
        for env_var in env_vars:
            api_key = os.getenv(env_var)
            if api_key:
                return api_key
        
        raise ValueError(f"No API key found in environment variables: {env_vars}")
    
    def get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Get authentication headers with API key
        
        Args:
            additional_headers (dict, optional): Additional headers to include
            
        Returns:
            dict: Headers with authentication
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        if additional_headers:
            headers.update(additional_headers)
            
        return headers
    
    def validate_api_key(self) -> bool:
        """
        Validate API key by making a test request
        
        Returns:
            bool: True if API key is valid
        """
        try:
            # Use a simple endpoint to test authentication
            test_url = self.config[self.environment].get("key_generate_url", "")
            if not test_url:
                return False
                
            headers = self.get_headers()
            response = requests.get(test_url, headers=headers, timeout=10)
            
            return response.status_code in [200, 401, 403]  # 401/403 means key is recognized but unauthorized
            
        except Exception:
            return False
    
    def get_base_url(self, service: str = "portal") -> str:
        """
        Get base URL for different services
        
        Args:
            service (str): Service type ("portal", "inference", "image")
            
        Returns:
            str: Base URL for the service
        """
        if service == "portal":
            return self.config[self.environment].get("key_generate_url", "").replace("/api/v1/key/generate", "")
        elif service == "inference":
            return self.config[self.environment].get("base_url", "").replace("/v1/chat/completions", "")
        elif service == "image":
            return self.config[self.environment].get("image_base_url", "").replace("/api/v1/images/generation", "")
        else:
            raise ValueError(f"Unknown service: {service}")


def get_auth(environment: str = "staging", config_data: Optional[Dict[str, Any]] = None) -> NebulaAuth:
    """
    Factory function to get authentication instance
    
    Args:
        environment (str): Environment to use
        config_data (dict, optional): Pre-loaded config data
        
    Returns:
        NebulaAuth: Authentication instance
    """
    return NebulaAuth(environment, config_data)


def validate_environment(environment: str) -> bool:
    """
    Validate if environment exists in config
    
    Args:
        environment (str): Environment to validate
        
    Returns:
        bool: True if environment exists
    """
    try:
        with open("config.yaml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return environment in config
    except Exception:
        return False


def list_available_environments() -> list:
    """
    List available environments from config
    
    Returns:
        list: List of available environments
    """
    try:
        with open("config.yaml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return list(config.keys())
    except Exception:
        return []

def login_user(user_id: str) -> str:
    """
    Login user and return JWT token.
    
    Args:
        user_id: User ID from data/users.json (e.g., "Member9", "Ellie")
        
    Returns:
        JWT token string
        
    Raises:
        Exception: If login fails
    """
    import json
    from pathlib import Path
    
    # Load users from JSON
    users_file = Path(__file__).parent.parent / "data" / "users.json"
    with open(users_file, "r", encoding="utf-8") as f:
        users = json.load(f)
    
    if user_id not in users:
        raise Exception(f"User '{user_id}' not found in users.json")
    
    user_data = users[user_id]
    
    # Load config
    config_file = Path(__file__).parent.parent / "config.yaml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    
    base_url = config["base_url"]
    
    # Login request
    payload = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    
    response = requests.post(f"{base_url}/login", data=payload, timeout=10)
    
    if response.status_code == 200:
        response_data = response.json()
        if "data" in response_data and "jwtToken" in response_data["data"]:
            return response_data["data"]["jwtToken"]
        else:
            raise Exception(f"Login response missing jwtToken: {response.text}")
    else:
        raise Exception(f"Login failed: {response.status_code} - {response.text}") 