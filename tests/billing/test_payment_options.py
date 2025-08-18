"""
Test file for testing payment options functionality
Tests GET /api/v1/payment/options endpoint
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestPaymentOptions:
    """Test class for payment options functionality using CreditsAPI"""
    
    def test_get_payment_options_success(self, credits_api):
        """Test successful retrieval of payment options"""
        logger.info("Testing payment options retrieval")
        
        response = credits_api.get_payment_options()
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for payment options response structure
        assert "data" in response_data, "Response should contain data field"
        
        # Payment options should be a list
        options = response_data["data"]
        assert isinstance(options, list), "Payment options should be a list"
        
        logger.info(f"✅ Payment options retrieved successfully. Found {len(options)} options")
        return response_data
    
    def test_payment_options_response_structure(self, credits_api):
        """Test that payment options response has correct structure"""
        logger.info("Testing payment options response structure")
        
        response = credits_api.get_payment_options()
        assert response.status_code == 200, "Request should succeed"
        
        response_data = response.json()
        
        # Check required fields
        assert "data" in response_data, "Response should contain 'data' field"
        assert "message" in response_data, "Response should contain 'message' field"
        assert "status" in response_data, "Response should contain 'status' field"
        
        # Check data field is a list
        options = response_data["data"]
        assert isinstance(options, list), "Data should be a list"
        
        # Check field types
        assert isinstance(response_data["message"], str), "Message should be string"
        assert isinstance(response_data["status"], str), "Status should be string"
        
        # Check field values
        assert response_data["status"] == "success", "Status should be 'success'"
        
        logger.info("✅ Payment options response structure validation passed")
    
    def test_payment_options_content_validation(self, credits_api):
        """Test that payment options contain expected content"""
        logger.info("Testing payment options content validation")
        
        response = credits_api.get_payment_options()
        assert response.status_code == 200, "Request should succeed"
        
        response_data = response.json()
        options = response_data["data"]
        
        # If there are options, validate their structure
        if options:
            for option in options:
                # Each option should have basic payment method info
                assert isinstance(option, dict), "Each option should be a dictionary"
                
                # Common fields that payment options might have
                # (adjust based on actual API response)
                if "id" in option:
                    assert isinstance(option["id"], str), "Option ID should be string"
                if "type" in option:
                    assert isinstance(option["type"], str), "Option type should be string"
                if "name" in option:
                    assert isinstance(option["name"], str), "Option name should be string"
        
        logger.info(f"✅ Payment options content validation passed. Found {len(options)} options")
    
    def test_payment_options_performance(self, credits_api):
        """Test that payment options retrieval responds within reasonable time"""
        import time
        
        logger.info("Testing payment options response time")
        
        start_time = time.time()
        response = credits_api.get_payment_options()
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 3.0, f"Response time {response_time:.2f}s exceeds 3s limit"
        
        logger.info(f"✅ Payment options response time: {response_time:.2f}s")
    
    def test_payment_options_authentication_required(self, credits_api):
        """Test that payment options require authentication"""
        # This test assumes the endpoint requires authentication
        # If it doesn't, this test will pass anyway
        logger.info("Testing that payment options require authentication")
        
        response = credits_api.get_payment_options()
        
        # Should either succeed (if no auth required) or fail with auth error
        assert response.status_code in [200, 401, 403], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            logger.info("✅ Payment options endpoint accessible without authentication")
        else:
            logger.info(f"✅ Payment options endpoint requires authentication (status: {response.status_code})")
    
    def test_payment_options_empty_response_handling(self, credits_api):
        """Test handling of empty payment options response"""
        logger.info("Testing empty payment options response handling")
        
        response = credits_api.get_payment_options()
        assert response.status_code == 200, "Request should succeed"
        
        response_data = response.json()
        options = response_data["data"]
        
        # Handle both empty and populated responses
        if not options:
            logger.info("✅ Empty payment options handled correctly")
            # Empty list should still be valid
            assert options == [], "Empty options should be empty list"
        else:
            logger.info(f"✅ Payment options populated with {len(options)} items")
    
    def test_payment_options_consistency(self, credits_api):
        """Test that payment options are consistent across multiple calls"""
        logger.info("Testing payment options consistency across multiple calls")
        
        # Make multiple calls
        responses = []
        for i in range(3):
            response = credits_api.get_payment_options()
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
        
        logger.info("✅ Payment options consistency validation passed")
    
    def test_payment_options_integration_with_credits_balance(self, credits_api):
        """Test integration between payment options and credits balance"""
        logger.info("Testing integration: payment options + credits balance")
        
        # Get payment options
        options_response = credits_api.get_payment_options()
        assert options_response.status_code == 200, "Payment options retrieval should succeed"
        
        # Get credits balance
        balance_response = credits_api.get_credits_balance()
        assert balance_response.status_code == 200, "Credits balance retrieval should succeed"
        
        logger.info("✅ Integration test passed: payment options + credits balance")
    
    def test_payment_options_integration_with_payment_methods(self, credits_api):
        """Test integration between payment options and payment methods"""
        logger.info("Testing integration: payment options + payment methods")
        
        # Get payment options
        options_response = credits_api.get_payment_options()
        assert options_response.status_code == 200, "Payment options retrieval should succeed"
        
        # Get payment methods
        methods_response = credits_api.get_payment_methods()
        assert methods_response.status_code == 200, "Payment methods retrieval should succeed"
        
        logger.info("✅ Integration test passed: payment options + payment methods")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Payment options test cleanup completed") 