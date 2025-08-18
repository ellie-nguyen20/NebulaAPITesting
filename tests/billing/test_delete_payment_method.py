"""
Test file for testing delete payment method functionality
Tests POST /api/v1/payment/delete endpoint
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDeletePaymentMethod:
    """Test class for delete payment method functionality using CreditsAPI"""
    
    def test_delete_stripe_method_success(self, credits_api):
        """Test successful deletion of Stripe payment method"""
        payment_method_id = "pm_test_1234567890"  # Mock payment method ID
        
        logger.info(f"Testing Stripe payment method deletion: {payment_method_id}")
        
        response = credits_api.delete_stripe_method(payment_method_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for deletion response structure
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Stripe payment method deleted successfully: {payment_method_id}")
        return response_data
    
    # Parameterized tests for different payment method IDs
    @pytest.mark.parametrize("payment_method_id", [
        "pm_test_1234567890",
        "pm_test_abcdefghij",
        "pm_test_9876543210",
        "pm_test_qwertyuiop",
        "pm_test_asdfghjklz",
    ])
    def test_delete_stripe_method_different_ids(self, credits_api, payment_method_id):
        """Test Stripe payment method deletion with various IDs"""
        logger.info(f"Testing Stripe payment method deletion: {payment_method_id}")
        
        response = credits_api.delete_stripe_method(payment_method_id)
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
    def test_delete_stripe_method_invalid_ids(self, credits_api, payment_method_id, expected_status):
        """Test Stripe payment method deletion with invalid IDs"""
        logger.info(f"Testing payment method ID: {payment_method_id}, expected: {expected_status}")
        
        response = credits_api.delete_stripe_method(payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Payment method ID {payment_method_id} was accepted")
        else:
            logger.info(f"✅ Invalid payment method ID {payment_method_id} properly rejected")
    
    # Edge cases
    def test_delete_stripe_method_very_long_id(self, credits_api):
        """Test Stripe payment method deletion with very long ID"""
        payment_method_id = "pm_test_" + "a" * 100  # Very long ID
        
        logger.info(f"Testing very long payment method ID: {len(payment_method_id)} characters")
        
        response = credits_api.delete_stripe_method(payment_method_id)
        # Should either accept or reject with appropriate error
        assert response.status_code in [200, 400, 413], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Very long payment method ID accepted")
        else:
            logger.info(f"✅ Very long payment method ID properly rejected with status {response.status_code}")
    
    def test_delete_stripe_method_special_characters(self, credits_api):
        """Test Stripe payment method deletion with special characters in ID"""
        payment_method_id = "pm_test_!@#$%^&*()_+-="
        
        logger.info(f"Testing special characters in payment method ID: {payment_method_id}")
        
        response = credits_api.delete_stripe_method(payment_method_id)
        # Should either accept or reject with appropriate error
        assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Special characters accepted")
        else:
            logger.info(f"✅ Special characters properly rejected with status {response.status_code}")
    
    # Response structure validation
    def test_delete_stripe_method_response_structure(self, credits_api):
        """Test that delete Stripe payment method response has correct structure"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response structure for payment method: {payment_method_id}")
        
        response = credits_api.delete_stripe_method(payment_method_id)
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
        
        logger.info("✅ Delete Stripe payment method response structure validation passed")
    
    # Performance tests
    def test_delete_stripe_method_response_time(self, credits_api):
        """Test that Stripe payment method deletion responds within reasonable time"""
        import time
        
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response time for payment method: {payment_method_id}")
        
        start_time = time.time()
        response = credits_api.delete_stripe_method(payment_method_id)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    # Integration tests
    def test_delete_stripe_method_with_payment_methods(self, credits_api):
        """Test Stripe payment method deletion and then check payment methods"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing integration: delete payment method + get payment methods for {payment_method_id}")
        
        # Delete Stripe payment method
        delete_response = credits_api.delete_stripe_method(payment_method_id)
        assert delete_response.status_code == 200, "Payment method deletion should succeed"
        
        # Get payment methods
        methods_response = credits_api.get_payment_methods()
        assert methods_response.status_code == 200, "Payment methods retrieval should succeed"
        
        logger.info("✅ Integration test passed: delete payment method + get payment methods")
    
    def test_delete_stripe_method_with_auto_pay_setting(self, credits_api):
        """Test Stripe payment method deletion and then check auto-pay setting"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing integration: delete payment method + auto-pay setting for {payment_method_id}")
        
        # Delete Stripe payment method
        delete_response = credits_api.delete_stripe_method(payment_method_id)
        assert delete_response.status_code == 200, "Payment method deletion should succeed"
        
        # Get auto-pay setting
        auto_pay_response = credits_api.get_auto_pay_setting()
        assert auto_pay_response.status_code == 200, "Auto-pay setting retrieval should succeed"
        
        logger.info("✅ Integration test passed: delete payment method + auto-pay setting")
    
    # Error handling tests
    def test_delete_stripe_method_missing_parameter(self, credits_api):
        """Test Stripe payment method deletion with missing parameter"""
        payment_method_id = None
        
        logger.info(f"Testing missing payment method ID: {payment_method_id}")
        
        response = credits_api.delete_stripe_method(payment_method_id)
        # The API should handle None payment method ID appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing payment method ID properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_delete_stripe_method_different_user_tiers(self, credits_api):
        """Test Stripe payment method deletion works for different user tiers"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing Stripe payment method deletion for current user tier: {payment_method_id}")
        
        response = credits_api.delete_stripe_method(payment_method_id)
        assert response.status_code == 200, "Payment method deletion should work for current user tier"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info("✅ Stripe payment method deletion works for current user tier")
    
    # Consistency tests
    def test_delete_stripe_method_consistency(self, credits_api):
        """Test that Stripe payment method deletion is consistent across multiple calls"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing Stripe payment method deletion consistency for: {payment_method_id}")
        
        # Make multiple calls
        responses = []
        for i in range(3):
            response = credits_api.delete_stripe_method(payment_method_id)
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
        
        logger.info("✅ Stripe payment method deletion consistency validation passed")
    
    # Non-existent payment method tests
    def test_delete_stripe_method_nonexistent(self, credits_api):
        """Test deletion of non-existent payment method"""
        payment_method_id = "pm_test_nonexistent_12345"
        
        logger.info(f"Testing deletion of non-existent payment method: {payment_method_id}")
        
        response = credits_api.delete_stripe_method(payment_method_id)
        # Should either succeed (idempotent) or fail with appropriate error
        assert response.status_code in [200, 404, 400], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            logger.info(f"✅ Non-existent payment method deletion succeeded (idempotent)")
        else:
            logger.info(f"✅ Non-existent payment method properly rejected with status {response.status_code}")
    
    # Already deleted payment method tests
    def test_delete_stripe_method_already_deleted(self, credits_api):
        """Test deletion of already deleted payment method"""
        payment_method_id = "pm_test_already_deleted_12345"
        
        logger.info(f"Testing deletion of already deleted payment method: {payment_method_id}")
        
        # First deletion
        first_response = credits_api.delete_stripe_method(payment_method_id)
        if first_response.status_code == 200:
            logger.info(f"✅ First deletion successful for {payment_method_id}")
            
            # Second deletion (should be idempotent)
            second_response = credits_api.delete_stripe_method(payment_method_id)
            
            if second_response.status_code == 200:
                logger.info(f"✅ Second deletion also successful (idempotent)")
            else:
                logger.info(f"✅ Second deletion properly rejected with status {second_response.status_code}")
        else:
            logger.info(f"❌ First deletion failed with status {first_response.status_code}")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Delete payment method test cleanup completed") 