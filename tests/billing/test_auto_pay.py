"""
Test file for testing auto-pay functionality
Tests GET and PUT /api/v1/payment/auto-pay endpoints
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestAutoPay:
    """Test class for auto-pay functionality using CreditsAPI"""
    
    def test_get_auto_pay_setting_success(self, credits_api):
        """Test successful retrieval of auto-pay setting"""
        logger.info("Testing auto-pay setting retrieval")
        
        response = credits_api.get_auto_pay_setting()
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for auto-pay response structure
        assert "data" in response_data, "Response should contain data field"
        
        logger.info("✅ Auto-pay setting retrieved successfully")
        return response_data
    
    def test_update_auto_pay_setting_enable(self, credits_api):
        """Test enabling auto-pay setting"""
        enabled = True
        payment_method_id = "pm_test_1234567890"  # Mock payment method ID
        
        logger.info(f"Testing auto-pay enable: {enabled}, method: {payment_method_id}")
        
        response = credits_api.update_auto_pay_setting(enabled, payment_method_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Auto-pay enabled successfully")
        return response_data
    
    def test_update_auto_pay_setting_disable(self, credits_api):
        """Test disabling auto-pay setting"""
        enabled = False
        
        logger.info(f"Testing auto-pay disable: {enabled}")
        
        response = credits_api.update_auto_pay_setting(enabled)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Auto-pay disabled successfully")
        return response_data
    
    # Parameterized tests for different auto-pay settings
    @pytest.mark.parametrize("enabled,payment_method_id", [
        (True, "pm_test_1234567890"),
        (True, "pm_test_abcdefghij"),
        (False, None),
        (True, "pm_test_9876543210"),
        (False, None),
    ])
    def test_update_auto_pay_setting_different_configurations(self, credits_api, enabled, payment_method_id):
        """Test auto-pay setting updates with various configurations"""
        logger.info(f"Testing auto-pay: enabled={enabled}, method={payment_method_id}")
        
        response = credits_api.update_auto_pay_setting(enabled, payment_method_id)
        assert response.status_code == 200, f"Failed for enabled={enabled}, method={payment_method_id}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for enabled={enabled}, method={payment_method_id}"
        
        logger.info(f"✅ Success: enabled={enabled}, method={payment_method_id}")
    
    # Invalid enabled value tests
    @pytest.mark.parametrize("enabled,payment_method_id,expected_status", [
        ("invalid", "pm_test_1234567890", 400),    # String instead of boolean
        (None, "pm_test_1234567890", 400),         # None instead of boolean
        ("", "pm_test_1234567890", 400),           # Empty string
        (123, "pm_test_1234567890", 400),          # Number instead of boolean
        (True, "pm_test_1234567890", 200),         # Valid true
        (False, None, 200),                        # Valid false
    ])
    def test_update_auto_pay_setting_invalid_enabled_values(self, credits_api, enabled, payment_method_id, expected_status):
        """Test auto-pay setting updates with invalid enabled values"""
        logger.info(f"Testing invalid enabled: {enabled}, expected: {expected_status}")
        
        response = credits_api.update_auto_pay_setting(enabled, payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Invalid enabled value {enabled} was accepted (edge case)")
        else:
            logger.info(f"✅ Invalid enabled value {enabled} properly rejected")
    
    # Invalid payment method ID tests
    @pytest.mark.parametrize("enabled,payment_method_id,expected_status", [
        (True, "", 400),                          # Empty payment method ID
        (True, "invalid", 400),                   # Invalid payment method ID
        (True, "123", 400),                       # Numeric payment method ID
        (True, "pm_test_1234567890", 200),        # Valid payment method ID
        (True, "pm_test_abcdefghij", 200),        # Valid payment method ID with letters
    ])
    def test_update_auto_pay_setting_invalid_payment_methods(self, credits_api, enabled, payment_method_id, expected_status):
        """Test auto-pay setting updates with invalid payment method IDs"""
        logger.info(f"Testing payment method: {payment_method_id}, expected: {expected_status}")
        
        response = credits_api.update_auto_pay_setting(enabled, payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Payment method {payment_method_id} was accepted")
        else:
            logger.info(f"✅ Invalid payment method {payment_method_id} properly rejected")
    
    # Response structure validation
    def test_get_auto_pay_setting_response_structure(self, credits_api):
        """Test that get auto-pay setting response has correct structure"""
        logger.info("Testing get auto-pay setting response structure")
        
        response = credits_api.get_auto_pay_setting()
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
        
        logger.info("✅ Get auto-pay setting response structure validation passed")
    
    def test_update_auto_pay_setting_response_structure(self, credits_api):
        """Test that update auto-pay setting response has correct structure"""
        enabled = True
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing update auto-pay setting response structure for enabled={enabled}")
        
        response = credits_api.update_auto_pay_setting(enabled, payment_method_id)
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
        
        logger.info("✅ Update auto-pay setting response structure validation passed")
    
    # Performance tests
    def test_get_auto_pay_setting_response_time(self, credits_api):
        """Test that get auto-pay setting responds within reasonable time"""
        import time
        
        logger.info("Testing get auto-pay setting response time")
        
        start_time = time.time()
        response = credits_api.get_auto_pay_setting()
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 3.0, f"Response time {response_time:.2f}s exceeds 3s limit"
        
        logger.info(f"✅ Get auto-pay setting response time: {response_time:.2f}s")
    
    def test_update_auto_pay_setting_response_time(self, credits_api):
        """Test that update auto-pay setting responds within reasonable time"""
        import time
        
        enabled = True
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing update auto-pay setting response time for enabled={enabled}")
        
        start_time = time.time()
        response = credits_api.update_auto_pay_setting(enabled, payment_method_id)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Update auto-pay setting response time: {response_time:.2f}s")
    
    # Integration tests
    def test_auto_pay_setting_workflow(self, credits_api):
        """Test complete auto-pay setting workflow: get -> update -> get"""
        logger.info("Testing complete auto-pay setting workflow")
        
        # Step 1: Get current setting
        get_response = credits_api.get_auto_pay_setting()
        assert get_response.status_code == 200, "Get auto-pay setting should succeed"
        
        # Step 2: Update setting
        enabled = True
        payment_method_id = "pm_test_1234567890"
        update_response = credits_api.update_auto_pay_setting(enabled, payment_method_id)
        assert update_response.status_code == 200, "Update auto-pay setting should succeed"
        
        # Step 3: Get updated setting
        get_updated_response = credits_api.get_auto_pay_setting()
        assert get_updated_response.status_code == 200, "Get updated auto-pay setting should succeed"
        
        logger.info("✅ Auto-pay setting workflow test passed")
    
    def test_auto_pay_setting_with_payment_methods(self, credits_api):
        """Test auto-pay setting integration with payment methods"""
        logger.info("Testing auto-pay setting integration with payment methods")
        
        # Get auto-pay setting
        auto_pay_response = credits_api.get_auto_pay_setting()
        assert auto_pay_response.status_code == 200, "Auto-pay setting retrieval should succeed"
        
        # Get payment methods
        methods_response = credits_api.get_payment_methods()
        assert methods_response.status_code == 200, "Payment methods retrieval should succeed"
        
        logger.info("✅ Integration test passed: auto-pay setting + payment methods")
    
    # Error handling tests
    def test_update_auto_pay_setting_missing_parameters(self, credits_api):
        """Test auto-pay setting update with missing parameters"""
        # Test with None values for required parameters
        enabled = None
        payment_method_id = None
        
        logger.info(f"Testing missing parameters: enabled={enabled}, method={payment_method_id}")
        
        response = credits_api.update_auto_pay_setting(enabled, payment_method_id)
        # The API should handle None parameters appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing parameters properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_auto_pay_setting_different_user_tiers(self, credits_api):
        """Test auto-pay setting works for different user tiers"""
        logger.info("Testing auto-pay setting for current user tier")
        
        # Test get
        get_response = credits_api.get_auto_pay_setting()
        assert get_response.status_code == 200, "Get auto-pay setting should work for current user tier"
        
        # Test update
        enabled = False
        update_response = credits_api.update_auto_pay_setting(enabled)
        assert update_response.status_code == 200, "Update auto-pay setting should work for current user tier"
        
        logger.info("✅ Auto-pay setting works for current user tier")
    
    # Consistency tests
    def test_auto_pay_setting_consistency(self, credits_api):
        """Test that auto-pay setting operations are consistent across multiple calls"""
        logger.info("Testing auto-pay setting consistency across multiple calls")
        
        # Test get consistency
        get_responses = []
        for i in range(3):
            response = credits_api.get_auto_pay_setting()
            assert response.status_code == 200, f"Get request {i+1} should succeed"
            get_responses.append(response.json())
        
        # All get responses should have same structure
        first_get_response = get_responses[0]
        for i, response in enumerate(get_responses[1:], 1):
            assert "data" in response, f"Get response {i+1} should contain data field"
            assert "status" in response, f"Get response {i+1} should contain status field"
            assert response["status"] == first_get_response["status"], f"Status should be consistent across get calls"
        
        logger.info("✅ Auto-pay setting consistency validation passed")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Auto-pay test cleanup completed") 