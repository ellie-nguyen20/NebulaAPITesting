"""
Simple Authentication Token Fixtures
"""

import pytest
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def load_users_from_json():
    """Load user credentials from data/users.json"""
    try:
        with open("data/users.json", "r", encoding="utf-8") as file:
            users_data = json.load(file)
        return users_data
    except FileNotFoundError:
        raise FileNotFoundError("data/users.json not found. Please create this file with user credentials.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing data/users.json: {e}")

@pytest.fixture(scope="session")
def auth_token(config):
    """Get authentication token using config from conftest.py and users from data/users.json"""
    # Use the base_url from config (now it's portal API)
    base_url = config["base_url"]
    
    # Load users from JSON file
    users = load_users_from_json()
    
    # Use Ellie's credentials by default (or first available user)
    default_user = "Ellie" if "Ellie" in users else list(users.keys())[0]
    user_creds = users[default_user]
    
    # Login with /login endpoint
    try:
        print(f"Attempting login with endpoint: /login")
        payload = {"username": user_creds["email"], "password": user_creds["password"]}
        print(f"Login payload: {payload}")
        print(f"Base URL: {base_url}")
        resp = requests.post(f"{base_url}/login", data=payload, timeout=10)
        
        if resp.status_code == 200:
            response_data = resp.json()
            # Check if token is in data.jwtToken (actual response structure)
            if "data" in response_data and "jwtToken" in response_data["data"]:
                token = response_data["data"]["jwtToken"]
                print(f"Login successful with endpoint: /login")
                return token
            else:
                print(f"Login response missing jwtToken: {resp.text}")
        else:
            print(f"Login failed with endpoint /login: {resp.status_code} - {resp.text}")
            
    except Exception as e:
        print(f"Error with endpoint /login: {e}")
    
    # If login fails, raise error
    print("Login failed")
    raise Exception(f"Failed to login with endpoint /login. Status: {resp.status_code}, Response: {resp.text}")

@pytest.fixture(scope="module")
def user_credentials():
    """Get all user credentials from data/users.json"""
    return load_users_from_json()

