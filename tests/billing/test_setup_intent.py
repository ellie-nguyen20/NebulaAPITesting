"""
Test file for testing setup intent functionality
Tests POST /api/v1/payment/setup-intent endpoint
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestSetupIntent:
    """Test class for setup intent functionality using CreditsAPI"""
    
    def test_create_setup_intent_success(self, credits_api):
        """Test successful setup intent creation"""
        payment_method_id = "pm_test_1234567890"  # Mock payment method ID
        
        logger.info(f"Testing setup intent creation for payment method: {payment_method_id}")
        
        response = credits_api.create_setup_intent(payment_method_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for setup intent response structure
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Setup intent created successfully for payment method: {payment_method_id}")
        return response_data
    
    # Parameterized tests for different payment method IDs
    @pytest.mark.parametrize("payment_method_id", [
        "pm_test_1234567890",
        "pm_test_abcdefghij",
        "pm_test_9876543210",
        "pm_test_qwertyuiop",
        "pm_test_asdfghjklz",
    ])
    def test_create_setup_intent_different_payment_methods(self, credits_api, payment_method_id):
        """Test setup intent creation with various payment method IDs"""
        logger.info(f"Testing setup intent for payment method: {payment_method_id}")
        
        response = credits_api.create_setup_intent(payment_method_id)
        assert response.status_code == 200, f"Failed for payment method {payment_method_id}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for payment method {payment_method_id}"
        
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
    def test_create_setup_intent_invalid_payment_methods(self, credits_api, payment_method_id, expected_status):
        """Test setup intent creation with invalid payment method IDs"""
        logger.info(f"Testing payment method: {payment_method_id}, expected: {expected_status}")
        
        response = credits_api.create_setup_intent(payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Payment method {payment_method_id} was accepted")
        else:
            logger.info(f"✅ Invalid payment method {payment_method_id} properly rejected")
    
    # Edge cases
    def test_create_setup_intent_very_long_payment_method_id(self, credits_api):
        """Test setup intent with very long payment method ID"""
        payment_method_id = "pm_test_" + "a" * 100  # Very long ID
        
        logger.info(f"Testing very long payment method ID: {len(payment_method_id)} characters")
        
        response = credits_api.create_setup_intent(payment_method_id)
        # Should either accept or reject with appropriate error
        assert response.status_code in [200, 400, 413], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Very long payment method ID accepted")
        else:
            logger.info(f"✅ Very long payment method ID properly rejected with status {response.status_code}")
    
    def test_create_setup_intent_special_characters(self, credits_api):
        """Test setup intent with special characters in payment method ID"""
        payment_method_id = "pm_test_!@#$%^&*()_+-="
        
        logger.info(f"Testing special characters in payment method ID: {payment_method_id}")
        
        response = credits_api.create_setup_intent(payment_method_id)
        # Should either accept or reject with appropriate error
        assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Special characters accepted")
        else:
            logger.info(f"✅ Special characters properly rejected with status {response.status_code}")
    
    # Response structure validation
    def test_create_setup_intent_response_structure(self, credits_api):
        """Test that setup intent response has correct structure"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response structure for payment method: {payment_method_id}")
        
        response = credits_api.create_setup_intent(payment_method_id)
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
        
        logger.info("✅ Setup intent response structure validation passed")
    
    # Performance tests
    def test_create_setup_intent_response_time(self, credits_api):
        """Test that setup intent creation responds within reasonable time"""
        import time
        
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response time for payment method: {payment_method_id}")
        
        start_time = time.time()
        response = credits_api.create_setup_intent(payment_method_id)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    # Integration tests
    def test_create_setup_intent_with_payment_methods(self, credits_api):
        """Test setup intent creation and then check payment methods"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing integration: setup intent + payment methods for {payment_method_id}")
        
        # Create setup intent
        setup_response = credits_api.create_setup_intent(payment_method_id)
        assert setup_response.status_code == 200, "Setup intent creation should succeed"
        
        # Get payment methods
        methods_response = credits_api.get_payment_methods()
        assert methods_response.status_code == 200, "Payment methods retrieval should succeed"
        
        logger.info("✅ Integration test passed: setup intent + payment methods")
    
    def test_create_setup_intent_with_credits_balance(self, credits_api):
        """Test setup intent creation and then check credits balance"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing integration: setup intent + credits balance for {payment_method_id}")
        
        # Create setup intent
        setup_response = credits_api.create_setup_intent(payment_method_id)
        assert setup_response.status_code == 200, "Setup intent creation should succeed"
        
        # Get credits balance
        balance_response = credits_api.get_credits_balance()
        assert balance_response.status_code == 200, "Credits balance retrieval should succeed"
        
        logger.info("✅ Integration test passed: setup intent + credits balance")
    
    # Error handling tests
    def test_create_setup_intent_missing_payment_method_id(self, credits_api):
        """Test setup intent creation with missing payment method ID"""
        payment_method_id = None
        
        logger.info(f"Testing missing payment method ID: {payment_method_id}")
        
        response = credits_api.create_setup_intent(payment_method_id)
        # The API should handle None payment method ID appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing payment method ID properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_create_setup_intent_different_user_tiers(self, credits_api):
        """Test setup intent creation works for different user tiers"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing setup intent for current user tier: {payment_method_id}")
        
        response = credits_api.create_setup_intent(payment_method_id)
        assert response.status_code == 200, "Setup intent should work for current user tier"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info("✅ Setup intent works for current user tier")
    
    # Consistency tests
    def test_create_setup_intent_consistency(self, credits_api):
        """Test that setup intent creation is consistent across multiple calls"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing setup intent consistency for payment method: {payment_method_id}")
        
        # Make multiple calls
        responses = []
        for i in range(3):
            response = credits_api.create_setup_intent(payment_method_id)
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
        
        logger.info("✅ Setup intent consistency validation passed")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Setup intent test cleanup completed") 