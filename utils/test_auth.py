import pytest
import os
from auth import NebulaAuth, get_auth, validate_environment, list_available_environments


@pytest.fixture
def sample_config():
    """Sample config data for testing"""
    return {
        "staging": {
            "base_url": "https://dev-llm-proxy.nebulablock.com/v1/chat/completions",
            "key_generate_url": "https://dev-portal-api.nebulablock.com/api/v1/key/generate"
        }
    }


def test_auth_initialization_with_config(sample_config):
    """Test khởi tạo NebulaAuth với config data"""
    try:
        auth = NebulaAuth(environment="staging", config_data=sample_config)
        assert auth.environment == "staging"
        assert auth.config == sample_config
        print("✅ Auth initialization with config successful")
    except Exception as e:
        pytest.fail(f"Auth initialization with config failed: {e}")


def test_auth_initialization_without_config():
    """Test khởi tạo NebulaAuth không có config data (fallback)"""
    try:
        auth = NebulaAuth(environment="staging")
        assert auth.environment == "staging"
        assert auth.config is not None
        print("✅ Auth initialization without config successful (fallback)")
    except Exception as e:
        pytest.fail(f"Auth initialization without config failed: {e}")


def test_get_headers():
    """Test tạo headers với authentication"""
    try:
        auth = NebulaAuth(environment="staging")
        headers = auth.get_headers()
        
        assert "Content-Type" in headers
        assert "Accept" in headers
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Bearer ")
        
        print("✅ Headers generation successful")
    except Exception as e:
        pytest.fail(f"Headers generation failed: {e}")


def test_get_headers_with_additional():
    """Test tạo headers với additional headers"""
    try:
        auth = NebulaAuth(environment="staging")
        additional_headers = {"X-Custom-Header": "test-value"}
        headers = auth.get_headers(additional_headers)
        
        assert headers["X-Custom-Header"] == "test-value"
        assert "Authorization" in headers
        
        print("✅ Additional headers added successfully")
    except Exception as e:
        pytest.fail(f"Additional headers failed: {e}")


def test_validate_api_key():
    """Test validate API key"""
    try:
        auth = NebulaAuth(environment="staging")
        is_valid = auth.validate_api_key()
        
        # API key validation should return boolean
        assert isinstance(is_valid, bool)
        print(f"✅ API key validation result: {is_valid}")
    except Exception as e:
        pytest.fail(f"API key validation failed: {e}")


def test_get_base_url():
    """Test lấy base URL cho các services"""
    try:
        auth = NebulaAuth(environment="staging")
        
        # Test portal URL
        portal_url = auth.get_base_url("portal")
        assert portal_url is not None
        assert "nebulablock.com" in portal_url
        
        # Test inference URL
        inference_url = auth.get_base_url("inference")
        assert inference_url is not None
        
        print("✅ Base URL generation successful")
    except Exception as e:
        pytest.fail(f"Base URL generation failed: {e}")


def test_get_auth_factory_with_config(sample_config):
    """Test factory function get_auth với config"""
    try:
        auth = get_auth(environment="staging", config_data=sample_config)
        assert isinstance(auth, NebulaAuth)
        assert auth.environment == "staging"
        assert auth.config == sample_config
        print("✅ Factory function with config working correctly")
    except Exception as e:
        pytest.fail(f"Factory function with config failed: {e}")


def test_get_auth_factory_without_config():
    """Test factory function get_auth không có config"""
    try:
        auth = get_auth(environment="staging")
        assert isinstance(auth, NebulaAuth)
        assert auth.environment == "staging"
        print("✅ Factory function without config working correctly")
    except Exception as e:
        pytest.fail(f"Factory function without config failed: {e}")


def test_validate_environment():
    """Test validate environment"""
    # Test valid environment
    assert validate_environment("staging") == True
    assert validate_environment("production") == True
    
    # Test invalid environment
    assert validate_environment("invalid_env") == False
    
    print("✅ Environment validation working correctly")


def test_list_available_environments():
    """Test list available environments"""
    environments = list_available_environments()
    
    assert isinstance(environments, list)
    assert "staging" in environments
    assert "production" in environments
    
    print(f"✅ Available environments: {environments}")


def test_environment_variables():
    """Test các environment variables patterns"""
    auth = NebulaAuth(environment="staging")
    
    # Kiểm tra xem có API key nào được tìm thấy không
    assert auth.api_key is not None
    assert len(auth.api_key) > 0
    
    print("✅ Environment variables loaded correctly")


def test_error_handling():
    """Test xử lý lỗi"""
    # Test với environment không tồn tại
    try:
        auth = NebulaAuth(environment="nonexistent")
        pytest.fail("Should have raised an exception")
    except Exception as e:
        print(f"✅ Correctly handled invalid environment: {e}")


if __name__ == "__main__":
    print("🧪 Running authentication tests...")
    
    # Create sample config for standalone testing
    sample_config = {
        "staging": {
            "base_url": "https://dev-llm-proxy.nebulablock.com/v1/chat/completions",
            "key_generate_url": "https://dev-portal-api.nebulablock.com/api/v1/key/generate"
        }
    }
    
    test_auth_initialization_with_config(sample_config)
    test_auth_initialization_without_config()
    test_get_headers()
    test_get_headers_with_additional()
    test_validate_api_key()
    test_get_base_url()
    test_get_auth_factory_with_config(sample_config)
    test_get_auth_factory_without_config()
    test_validate_environment()
    test_list_available_environments()
    test_environment_variables()
    test_error_handling()
    
    print("✅ All authentication tests completed!") 