"""
Test file for testing payment methods functionality
Tests GET /api/v1/payment/payment-methods and PUT /api/v1/payment/payment-methods/default endpoints
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestPaymentMethods:
    """Test class for payment methods functionality using CreditsAPI"""
    
    def test_get_payment_methods_success(self, credits_api):
        """Test successful retrieval of payment methods"""
        logger.info("Testing payment methods retrieval")
        
        response = credits_api.get_payment_methods()
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for payment methods response structure
        assert "data" in response_data, "Response should contain data field"
        
        # Payment methods should be a list
        methods = response_data["data"]
        assert isinstance(methods, list), "Payment methods should be a list"
        
        logger.info(f"✅ Payment methods retrieved successfully. Found {len(methods)} methods")
        return response_data
    
    def test_update_default_payment_method_success(self, credits_api):
        """Test successful update of default payment method"""
        payment_method_id = "pm_test_1234567890"  # Mock payment method ID
        
        logger.info(f"Testing default payment method update: {payment_method_id}")
        
        response = credits_api.update_default_payment_method(payment_method_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Default payment method updated successfully: {payment_method_id}")
        return response_data
    
    # Parameterized tests for different payment method IDs
    @pytest.mark.parametrize("payment_method_id", [
        "pm_test_1234567890",
        "pm_test_abcdefghij",
        "pm_test_9876543210",
        "pm_test_qwertyuiop",
        "pm_test_asdfghjklz",
    ])
    def test_update_default_payment_method_different_ids(self, credits_api, payment_method_id):
        """Test default payment method update with various IDs"""
        logger.info(f"Testing default payment method update: {payment_method_id}")
        
        response = credits_api.update_default_payment_method(payment_method_id)
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
    def test_update_default_payment_method_invalid_ids(self, credits_api, payment_method_id, expected_status):
        """Test default payment method update with invalid IDs"""
        logger.info(f"Testing payment method ID: {payment_method_id}, expected: {expected_status}")
        
        response = credits_api.update_default_payment_method(payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Payment method ID {payment_method_id} was accepted")
        else:
            logger.info(f"✅ Invalid payment method ID {payment_method_id} properly rejected")
    
    # Response structure validation
    def test_get_payment_methods_response_structure(self, credits_api):
        """Test that get payment methods response has correct structure"""
        logger.info("Testing get payment methods response structure")
        
        response = credits_api.get_payment_methods()
        assert response.status_code == 200, "Request should succeed"
        
        response_data = response.json()
        
        # Check required fields
        assert "data" in response_data, "Response should contain 'data' field"
        assert "message" in response_data, "Response should contain 'message' field"
        assert "status" in response_data, "Response should contain 'status' field"
        
        # Check data field is a list
        methods = response_data["data"]
        assert isinstance(methods, list), "Data should be a list"
        
        # Check field types
        assert isinstance(response_data["message"], str), "Message should be string"
        assert isinstance(response_data["status"], str), "Status should be string"
        
        # Check field values
        assert response_data["status"] == "success", "Status should be 'success'"
        
        logger.info("✅ Get payment methods response structure validation passed")
    
    def test_update_default_payment_method_response_structure(self, credits_api):
        """Test that update default payment method response has correct structure"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing update default payment method response structure for {payment_method_id}")
        
        response = credits_api.update_default_payment_method(payment_method_id)
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
        
        logger.info("✅ Update default payment method response structure validation passed")
    
    # Performance tests
    def test_get_payment_methods_response_time(self, credits_api):
        """Test that get payment methods responds within reasonable time"""
        import time
        
        logger.info("Testing get payment methods response time")
        
        start_time = time.time()
        response = credits_api.get_payment_methods()
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 3.0, f"Response time {response_time:.2f}s exceeds 3s limit"
        
        logger.info(f"✅ Get payment methods response time: {response_time:.2f}s")
    
    def test_update_default_payment_method_response_time(self, credits_api):
        """Test that update default payment method responds within reasonable time"""
        import time
        
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing update default payment method response time for {payment_method_id}")
        
        start_time = time.time()
        response = credits_api.update_default_payment_method(payment_method_id)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Update default payment method response time: {response_time:.2f}s")
    
    # Integration tests
    def test_payment_methods_workflow(self, credits_api):
        """Test complete payment methods workflow: get -> update -> get"""
        logger.info("Testing complete payment methods workflow")
        
        # Step 1: Get current payment methods
        get_response = credits_api.get_payment_methods()
        assert get_response.status_code == 200, "Get payment methods should succeed"
        
        # Step 2: Update default payment method
        payment_method_id = "pm_test_1234567890"
        update_response = credits_api.update_default_payment_method(payment_method_id)
        assert update_response.status_code == 200, "Update default payment method should succeed"
        
        # Step 3: Get updated payment methods
        get_updated_response = credits_api.get_payment_methods()
        assert get_updated_response.status_code == 200, "Get updated payment methods should succeed"
        
        logger.info("✅ Payment methods workflow test passed")
    
    def test_payment_methods_with_auto_pay_setting(self, credits_api):
        """Test payment methods integration with auto-pay setting"""
        logger.info("Testing payment methods integration with auto-pay setting")
        
        # Get payment methods
        methods_response = credits_api.get_payment_methods()
        assert methods_response.status_code == 200, "Payment methods retrieval should succeed"
        
        # Get auto-pay setting
        auto_pay_response = credits_api.get_auto_pay_setting()
        assert auto_pay_response.status_code == 200, "Auto-pay setting retrieval should succeed"
        
        logger.info("✅ Integration test passed: payment methods + auto-pay setting")
    
    def test_payment_methods_with_payment_options(self, credits_api):
        """Test payment methods integration with payment options"""
        logger.info("Testing payment methods integration with payment options")
        
        # Get payment methods
        methods_response = credits_api.get_payment_methods()
        assert methods_response.status_code == 200, "Payment methods retrieval should succeed"
        
        # Get payment options
        options_response = credits_api.get_payment_options()
        assert options_response.status_code == 200, "Payment options retrieval should succeed"
        
        logger.info("✅ Integration test passed: payment methods + payment options")
    
    # Error handling tests
    def test_update_default_payment_method_missing_parameter(self, credits_api):
        """Test default payment method update with missing parameter"""
        payment_method_id = None
        
        logger.info(f"Testing missing payment method ID: {payment_method_id}")
        
        response = credits_api.update_default_payment_method(payment_method_id)
        # The API should handle None payment method ID appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing payment method ID properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_payment_methods_different_user_tiers(self, credits_api):
        """Test payment methods operations work for different user tiers"""
        logger.info("Testing payment methods for current user tier")
        
        # Test get
        get_response = credits_api.get_payment_methods()
        assert get_response.status_code == 200, "Get payment methods should work for current user tier"
        
        # Test update default
        payment_method_id = "pm_test_1234567890"
        update_response = credits_api.update_default_payment_method(payment_method_id)
        assert update_response.status_code == 200, "Update default payment method should work for current user tier"
        
        logger.info("✅ Payment methods operations work for current user tier")
    
    # Content validation tests
    def test_payment_methods_content_validation(self, credits_api):
        """Test that payment methods contain expected content"""
        logger.info("Testing payment methods content validation")
        
        response = credits_api.get_payment_methods()
        assert response.status_code == 200, "Request should succeed"
        
        response_data = response.json()
        methods = response_data["data"]
        
        # If there are methods, validate their structure
        if methods:
            for method in methods:
                # Each method should have basic payment method info
                assert isinstance(method, dict), "Each method should be a dictionary"
                
                # Common fields that payment methods might have
                # (adjust based on actual API response)
                if "id" in method:
                    assert isinstance(method["id"], str), "Method ID should be string"
                if "type" in method:
                    assert isinstance(method["type"], str), "Method type should be string"
                if "card" in method:
                    assert isinstance(method["card"], dict), "Card info should be dictionary"
        
        logger.info(f"✅ Payment methods content validation passed. Found {len(methods)} methods")
    
    # Consistency tests
    def test_payment_methods_consistency(self, credits_api):
        """Test that payment methods operations are consistent across multiple calls"""
        logger.info("Testing payment methods consistency across multiple calls")
        
        # Test get consistency
        get_responses = []
        for i in range(3):
            response = credits_api.get_payment_methods()
            assert response.status_code == 200, f"Get request {i+1} should succeed"
            get_responses.append(response.json())
        
        # All get responses should have same structure
        first_get_response = get_responses[0]
        for i, response in enumerate(get_responses[1:], 1):
            assert "data" in response, f"Get response {i+1} should contain data field"
            assert "status" in response, f"Get response {i+1} should contain status field"
            assert response["status"] == first_get_response["status"], f"Status should be consistent across get calls"
        
        logger.info("✅ Payment methods consistency validation passed")
    
    # Edge cases
    def test_payment_methods_empty_response_handling(self, credits_api):
        """Test handling of empty payment methods response"""
        logger.info("Testing empty payment methods response handling")
        
        response = credits_api.get_payment_methods()
        assert response.status_code == 200, "Request should succeed"
        
        response_data = response.json()
        methods = response_data["data"]
        
        # Handle both empty and populated responses
        if not methods:
            logger.info("✅ Empty payment methods handled correctly")
            # Empty list should still be valid
            assert methods == [], "Empty methods should be empty list"
        else:
            logger.info(f"✅ Payment methods populated with {len(methods)} items")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Payment methods test cleanup completed") 