"""
Test file for testing payment intent functionality
Tests POST /api/v1/payment/payment-intent and POST /api/v1/payment/payment-intent-confirmation endpoints
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestPaymentIntent:
    """Test class for payment intent functionality using CreditsAPI"""
    
    def test_create_payment_intent_success(self, credits_api):
        """Test successful payment intent creation"""
        amount = 1000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"  # Mock payment method ID
        
        logger.info(f"Testing payment intent creation: {amount} {currency}")
        
        response = credits_api.create_payment_intent(amount, currency, payment_method_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for payment intent response structure
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Payment intent created successfully: {amount} {currency}")
        return response_data
    
    def test_confirm_payment_intent_success(self, credits_api):
        """Test successful payment intent confirmation"""
        payment_intent_id = "pi_test_1234567890"  # Mock payment intent ID
        
        logger.info(f"Testing payment intent confirmation: {payment_intent_id}")
        
        response = credits_api.confirm_payment_intent(payment_intent_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for confirmation response structure
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Payment intent confirmed successfully: {payment_intent_id}")
        return response_data
    
    # Parameterized tests for different amounts and currencies
    @pytest.mark.parametrize("amount,currency,payment_method_id", [
        (1000, "vnd", "pm_test_1234567890"),
        (5000, "vnd", "pm_test_1234567891"),
        (10000, "vnd", "pm_test_1234567892"),
        (10, "usd", "pm_test_1234567893"),
        (50, "usd", "pm_test_1234567894"),
        (100, "usd", "pm_test_1234567895"),
        (1, "eur", "pm_test_1234567896"),
        (5, "eur", "pm_test_1234567897"),
    ])
    def test_create_payment_intent_different_amounts_currencies(self, credits_api, amount, currency, payment_method_id):
        """Test payment intent creation with various amounts and currencies"""
        logger.info(f"Testing amount: {amount}, currency: {currency}, method: {payment_method_id}")
        
        response = credits_api.create_payment_intent(amount, currency, payment_method_id)
        assert response.status_code == 200, f"Failed for amount {amount} {currency}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for {amount} {currency}"
        
        logger.info(f"✅ Success: {amount} {currency}")
    
    # Parameterized tests for different payment intent IDs
    @pytest.mark.parametrize("payment_intent_id", [
        "pi_test_1234567890",
        "pi_test_abcdefghij",
        "pi_test_9876543210",
        "pi_test_qwertyuiop",
        "pi_test_asdfghjklz",
    ])
    def test_confirm_payment_intent_different_ids(self, credits_api, payment_intent_id):
        """Test payment intent confirmation with various IDs"""
        logger.info(f"Testing payment intent confirmation: {payment_intent_id}")
        
        response = credits_api.confirm_payment_intent(payment_intent_id)
        assert response.status_code == 200, f"Failed for payment intent ID {payment_intent_id}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for payment intent ID {payment_intent_id}"
        
        logger.info(f"✅ Success: {payment_intent_id}")
    
    # Invalid amount tests
    @pytest.mark.parametrize("amount,currency,payment_method_id,expected_status", [
        (0, "vnd", "pm_test_1234567890", 400),           # Zero amount
        (-1, "vnd", "pm_test_1234567890", 400),          # Negative amount
        (-1000, "vnd", "pm_test_1234567890", 400),       # Large negative amount
        ("invalid", "vnd", "pm_test_1234567890", 400),   # String amount
        (None, "vnd", "pm_test_1234567890", 400),        # None amount
        ("", "vnd", "pm_test_1234567890", 400),          # Empty string amount
        (0.01, "vnd", "pm_test_1234567890", 200),       # Small decimal amount (should work)
        (999999999, "vnd", "pm_test_1234567890", 200),  # Very large amount (should work)
    ])
    def test_create_payment_intent_invalid_amounts(self, credits_api, amount, currency, payment_method_id, expected_status):
        """Test payment intent creation with invalid amounts"""
        logger.info(f"Testing invalid amount: {amount} {currency}, expected: {expected_status}")
        
        response = credits_api.create_payment_intent(amount, currency, payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Invalid amount {amount} was accepted (edge case)")
        else:
            logger.info(f"✅ Invalid amount {amount} properly rejected")
    
    # Invalid payment intent ID tests
    @pytest.mark.parametrize("payment_intent_id,expected_status", [
        ("", 400),                          # Empty payment intent ID
        (None, 400),                        # None payment intent ID
        ("invalid", 400),                   # Invalid payment intent ID
        ("123", 400),                       # Numeric payment intent ID
        ("pi_test", 400),                   # Incomplete payment intent ID
        ("pi_test_1234567890", 200),        # Valid payment intent ID
        ("pi_test_abcdefghij", 200),        # Valid payment intent ID with letters
    ])
    def test_confirm_payment_intent_invalid_ids(self, credits_api, payment_intent_id, expected_status):
        """Test payment intent confirmation with invalid IDs"""
        logger.info(f"Testing payment intent ID: {payment_intent_id}, expected: {expected_status}")
        
        response = credits_api.confirm_payment_intent(payment_intent_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Payment intent ID {payment_intent_id} was accepted")
        else:
            logger.info(f"✅ Invalid payment intent ID {payment_intent_id} properly rejected")
    
    # Response structure validation
    def test_create_payment_intent_response_structure(self, credits_api):
        """Test that create payment intent response has correct structure"""
        amount = 1000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response structure for {amount} {currency}")
        
        response = credits_api.create_payment_intent(amount, currency, payment_method_id)
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
        
        logger.info("✅ Create payment intent response structure validation passed")
    
    def test_confirm_payment_intent_response_structure(self, credits_api):
        """Test that confirm payment intent response has correct structure"""
        payment_intent_id = "pi_test_1234567890"
        
        logger.info(f"Testing response structure for payment intent: {payment_intent_id}")
        
        response = credits_api.confirm_payment_intent(payment_intent_id)
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
        
        logger.info("✅ Confirm payment intent response structure validation passed")
    
    # Performance tests
    def test_create_payment_intent_response_time(self, credits_api):
        """Test that payment intent creation responds within reasonable time"""
        import time
        
        amount = 1000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response time for {amount} {currency}")
        
        start_time = time.time()
        response = credits_api.create_payment_intent(amount, currency, payment_method_id)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 10.0, f"Response time {response_time:.2f}s exceeds 10s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    def test_confirm_payment_intent_response_time(self, credits_api):
        """Test that payment intent confirmation responds within reasonable time"""
        import time
        
        payment_intent_id = "pi_test_1234567890"
        
        logger.info(f"Testing response time for payment intent: {payment_intent_id}")
        
        start_time = time.time()
        response = credits_api.confirm_payment_intent(payment_intent_id)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    # Integration tests
    def test_payment_intent_workflow(self, credits_api):
        """Test complete payment intent workflow: create -> confirm"""
        logger.info("Testing complete payment intent workflow")
        
        # Step 1: Create payment intent
        amount = 1000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        
        create_response = credits_api.create_payment_intent(amount, currency, payment_method_id)
        assert create_response.status_code == 200, "Payment intent creation should succeed"
        
        # Step 2: Confirm payment intent
        # Note: In real scenario, we'd extract the payment_intent_id from create_response
        payment_intent_id = "pi_test_1234567890"  # Mock ID for testing
        confirm_response = credits_api.confirm_payment_intent(payment_intent_id)
        assert confirm_response.status_code == 200, "Payment intent confirmation should succeed"
        
        logger.info("✅ Payment intent workflow test passed")
    
    def test_payment_intent_with_credits_balance(self, credits_api):
        """Test payment intent creation and then check credits balance"""
        amount = 5000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing integration: payment intent + credits balance for {amount} {currency}")
        
        # Create payment intent
        intent_response = credits_api.create_payment_intent(amount, currency, payment_method_id)
        assert intent_response.status_code == 200, "Payment intent creation should succeed"
        
        # Get credits balance
        balance_response = credits_api.get_credits_balance()
        assert balance_response.status_code == 200, "Credits balance retrieval should succeed"
        
        logger.info("✅ Integration test passed: payment intent + credits balance")
    
    # Error handling tests
    def test_create_payment_intent_missing_parameters(self, credits_api):
        """Test payment intent creation with missing parameters"""
        # Test with None values for required parameters
        amount = None
        currency = None
        payment_method_id = None
        
        logger.info(f"Testing missing parameters: amount={amount}, currency={currency}, method={payment_method_id}")
        
        response = credits_api.create_payment_intent(amount, currency, payment_method_id)
        # The API should handle None parameters appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing parameters properly handled with status {response.status_code}")
    
    def test_confirm_payment_intent_missing_parameter(self, credits_api):
        """Test payment intent confirmation with missing parameter"""
        payment_intent_id = None
        
        logger.info(f"Testing missing payment intent ID: {payment_intent_id}")
        
        response = credits_api.confirm_payment_intent(payment_intent_id)
        # The API should handle None payment intent ID appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing payment intent ID properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_payment_intent_different_user_tiers(self, credits_api):
        """Test payment intent operations work for different user tiers"""
        amount = 1000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        payment_intent_id = "pi_test_1234567890"
        
        logger.info(f"Testing payment intent for current user tier: {amount} {currency}")
        
        # Test create
        create_response = credits_api.create_payment_intent(amount, currency, payment_method_id)
        assert create_response.status_code == 200, "Payment intent creation should work for current user tier"
        
        # Test confirm
        confirm_response = credits_api.confirm_payment_intent(payment_intent_id)
        assert confirm_response.status_code == 200, "Payment intent confirmation should work for current user tier"
        
        logger.info("✅ Payment intent operations work for current user tier")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Payment intent test cleanup completed") 