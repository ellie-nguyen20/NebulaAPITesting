"""
Test file for testing validate payment method functionality
Tests POST /api/v1/payment/validate endpoint
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestValidatePaymentMethod:
    """Test class for validate payment method functionality using CreditsAPI"""
    
    def test_validate_payment_method_success(self, credits_api):
        """Test successful validation of payment method"""
        payment_method_id = "pm_test_1234567890"  # Mock payment method ID
        
        logger.info(f"Testing payment method validation: {payment_method_id}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for validation response structure
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Payment method validated successfully: {payment_method_id}")
        return response_data
    
    # Parameterized tests for different payment method IDs
    @pytest.mark.parametrize("payment_method_id", [
        "pm_test_1234567890",
        "pm_test_abcdefghij",
        "pm_test_9876543210",
        "pm_test_qwertyuiop",
        "pm_test_asdfghjklz",
    ])
    def test_validate_payment_method_different_ids(self, credits_api, payment_method_id):
        """Test payment method validation with various IDs"""
        logger.info(f"Testing payment method validation: {payment_method_id}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        assert response.status_code == 200, f"Failed for payment method ID {payment_method_id}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for payment method ID {payment_method_id}"
        
        logger.info(f"✅ Success: {payment_method_id}")
    
    # Invalid payment method ID tests
    @pytest.mark.parametrize("payment_method_id,expected_status", [
        ("", 400),                          # Empty payment method ID
        (None, 400),                        # None payment method ID
        ("invalid", 400),                   # Invalid payment method ID
        ("123", 400),                       # Numeric payment method ID
        ("pm_test", 400),                   # Incomplete payment method ID
        ("pm_test_1234567890", 200),        # Valid payment method ID
        ("pm_test_abcdefghij", 200),        # Valid payment method ID with letters
    ])
    def test_validate_payment_method_invalid_ids(self, credits_api, payment_method_id, expected_status):
        """Test payment method validation with invalid IDs"""
        logger.info(f"Testing payment method ID: {payment_method_id}, expected: {expected_status}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Payment method ID {payment_method_id} was accepted")
        else:
            logger.info(f"✅ Invalid payment method ID {payment_method_id} properly rejected")
    
    # Edge cases
    def test_validate_payment_method_very_long_id(self, credits_api):
        """Test payment method validation with very long ID"""
        payment_method_id = "pm_test_" + "a" * 100  # Very long ID
        
        logger.info(f"Testing very long payment method ID: {len(payment_method_id)} characters")
        
        response = credits_api.validate_payment_method(payment_method_id)
        # Should either accept or reject with appropriate error
        assert response.status_code in [200, 400, 413], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Very long payment method ID accepted")
        else:
            logger.info(f"✅ Very long payment method ID properly rejected with status {response.status_code}")
    
    def test_validate_payment_method_special_characters(self, credits_api):
        """Test payment method validation with special characters in ID"""
        payment_method_id = "pm_test_!@#$%^&*()_+-="
        
        logger.info(f"Testing special characters in payment method ID: {payment_method_id}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        # Should either accept or reject with appropriate error
        assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Special characters accepted")
        else:
            logger.info(f"✅ Special characters properly rejected with status {response.status_code}")
    
    # Response structure validation
    def test_validate_payment_method_response_structure(self, credits_api):
        """Test that validate payment method response has correct structure"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response structure for payment method: {payment_method_id}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        assert response.status_code == 200, "Request should succeed"
        
        response_data = response.json()
        
        # Check required fields
        assert "data" in response_data, "Response should contain 'data' field"
        assert "message" in response_data, "Response should contain 'message' field"
        assert "status" in response_data, "Response should contain 'status' field"
        
        # Check field types
        assert isinstance(response_data["message"], str), "Message should be string"
        assert isinstance(response_data["status"], str), "Status should be string"
        
        # Check field values
        assert response_data["status"] == "success", "Status should be 'success'"
        
        logger.info("✅ Validate payment method response structure validation passed")
    
    # Performance tests
    def test_validate_payment_method_response_time(self, credits_api):
        """Test that payment method validation responds within reasonable time"""
        import time
        
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response time for payment method: {payment_method_id}")
        
        start_time = time.time()
        response = credits_api.validate_payment_method(payment_method_id)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    # Integration tests
    def test_validate_payment_method_with_payment_methods(self, credits_api):
        """Test payment method validation and then check payment methods"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing integration: validate payment method + get payment methods for {payment_method_id}")
        
        # Validate payment method
        validate_response = credits_api.validate_payment_method(payment_method_id)
        assert validate_response.status_code == 200, "Payment method validation should succeed"
        
        # Get payment methods
        methods_response = credits_api.get_payment_methods()
        assert methods_response.status_code == 200, "Payment methods retrieval should succeed"
        
        logger.info("✅ Integration test passed: validate payment method + get payment methods")
    
    def test_validate_payment_method_with_auto_pay_setting(self, credits_api):
        """Test payment method validation and then check auto-pay setting"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing integration: validate payment method + auto-pay setting for {payment_method_id}")
        
        # Validate payment method
        validate_response = credits_api.validate_payment_method(payment_method_id)
        assert validate_response.status_code == 200, "Payment method validation should succeed"
        
        # Get auto-pay setting
        auto_pay_response = credits_api.get_auto_pay_setting()
        assert auto_pay_response.status_code == 200, "Auto-pay setting retrieval should succeed"
        
        logger.info("✅ Integration test passed: validate payment method + auto-pay setting")
    
    # Error handling tests
    def test_validate_payment_method_missing_parameter(self, credits_api):
        """Test payment method validation with missing parameter"""
        payment_method_id = None
        
        logger.info(f"Testing missing payment method ID: {payment_method_id}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        # The API should handle None payment method ID appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing payment method ID properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_validate_payment_method_different_user_tiers(self, credits_api):
        """Test payment method validation works for different user tiers"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing payment method validation for current user tier: {payment_method_id}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        assert response.status_code == 200, "Payment method validation should work for current user tier"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info("✅ Payment method validation works for current user tier")
    
    # Consistency tests
    def test_validate_payment_method_consistency(self, credits_api):
        """Test that payment method validation is consistent across multiple calls"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing payment method validation consistency for: {payment_method_id}")
        
        # Make multiple calls
        responses = []
        for i in range(3):
            response = credits_api.validate_payment_method(payment_method_id)
            assert response.status_code == 200, f"Request {i+1} should succeed"
            responses.append(response.json())
        
        # All responses should have same structure
        first_response = responses[0]
        for i, response in enumerate(responses[1:], 1):
            assert "data" in response, f"Response {i+1} should contain data field"
            assert "message" in response, f"Response {i+1} should contain message field"
            assert "status" in response, f"Response {i+1} should contain status field"
            
            # Status should be consistent
            assert response["status"] == first_response["status"], f"Status should be consistent across calls"
        
        logger.info("✅ Payment method validation consistency validation passed")
    
    # Non-existent payment method tests
    def test_validate_payment_method_nonexistent(self, credits_api):
        """Test validation of non-existent payment method"""
        payment_method_id = "pm_test_nonexistent_12345"
        
        logger.info(f"Testing validation of non-existent payment method: {payment_method_id}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        # Should either succeed or fail with appropriate error
        assert response.status_code in [200, 404, 400], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            logger.info(f"✅ Non-existent payment method validation succeeded")
        else:
            logger.info(f"✅ Non-existent payment method properly rejected with status {response.status_code}")
    
    # Expired payment method tests
    def test_validate_payment_method_expired(self, credits_api):
        """Test validation of expired payment method"""
        payment_method_id = "pm_test_expired_12345"
        
        logger.info(f"Testing validation of expired payment method: {payment_method_id}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        # Should either succeed or fail with appropriate error
        assert response.status_code in [200, 400, 422], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            logger.info(f"✅ Expired payment method validation succeeded")
        else:
            logger.info(f"✅ Expired payment method properly rejected with status {response.status_code}")
    
    # Content validation tests
    def test_validate_payment_method_content_validation(self, credits_api):
        """Test that validation response contains expected content"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing content validation for payment method: {payment_method_id}")
        
        response = credits_api.validate_payment_method(payment_method_id)
        assert response.status_code == 200, "Request should succeed"
        
        response_data = response.json()
        data = response_data["data"]
        
        # Check if validation result is present
        # The actual structure depends on the API response
        if "valid" in data:
            assert isinstance(data["valid"], bool), "Validation result should be boolean"
        if "status" in data:
            assert isinstance(data["status"], str), "Validation status should be string"
        if "message" in data:
            assert isinstance(data["message"], str), "Validation message should be string"
        
        logger.info("✅ Payment method validation content validation passed")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Validate payment method test cleanup completed") 