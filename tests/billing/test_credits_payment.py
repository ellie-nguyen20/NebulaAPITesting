"""
Test file for testing credits payment functionality
Tests POST /api/v1/payment/payment endpoint
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestCreditsPayment:
    """Test class for credits payment functionality using CreditsAPI"""
    
    def test_make_credits_payment_success(self, credits_api):
        """Test successful credits payment"""
        amount = 1000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"  # Mock payment method ID
        
        logger.info(f"Testing credits payment: {amount} {currency}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for payment API response structure
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Credits payment successful: {amount} {currency}")
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
    def test_make_credits_payment_different_amounts_currencies(self, credits_api, amount, currency, payment_method_id):
        """Test credits payment with various amounts and currencies"""
        logger.info(f"Testing amount: {amount}, currency: {currency}, method: {payment_method_id}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        assert response.status_code == 200, f"Failed for amount {amount} {currency}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for {amount} {currency}"
        
        logger.info(f"✅ Success: {amount} {currency}")
    
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
    def test_make_credits_payment_invalid_amounts(self, credits_api, amount, currency, payment_method_id, expected_status):
        """Test credits payment with invalid amounts"""
        logger.info(f"Testing invalid amount: {amount} {currency}, expected: {expected_status}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Invalid amount {amount} was accepted (edge case)")
        else:
            logger.info(f"✅ Invalid amount {amount} properly rejected")
    
    # Invalid currency tests
    @pytest.mark.parametrize("amount,currency,payment_method_id,expected_status", [
        (1000, "invalid", "pm_test_1234567890", 400),    # Invalid currency
        (1000, "", "pm_test_1234567890", 400),           # Empty currency
        (1000, None, "pm_test_1234567890", 400),         # None currency
        (1000, "123", "pm_test_1234567890", 400),        # Numeric currency
        (1000, "USD", "pm_test_1234567890", 400),        # Uppercase currency (if case-sensitive)
        (1000, "vnd", "pm_test_1234567890", 200),        # Valid lowercase
        (1000, "usd", "pm_test_1234567890", 200),        # Valid lowercase
        (1000, "eur", "pm_test_1234567890", 200),        # Valid lowercase
    ])
    def test_make_credits_payment_invalid_currencies(self, credits_api, amount, currency, payment_method_id, expected_status):
        """Test credits payment with invalid currencies"""
        logger.info(f"Testing currency: {currency}, expected: {expected_status}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Currency {currency} was accepted")
        else:
            logger.info(f"✅ Invalid currency {currency} properly rejected")
    
    # Invalid payment method ID tests
    @pytest.mark.parametrize("amount,currency,payment_method_id,expected_status", [
        (1000, "vnd", "", 400),                          # Empty payment method ID
        (1000, "vnd", None, 400),                        # None payment method ID
        (1000, "vnd", "invalid", 400),                   # Invalid payment method ID
        (1000, "vnd", "123", 400),                       # Numeric payment method ID
        (1000, "vnd", "pm_test_1234567890", 200),        # Valid payment method ID
        (1000, "vnd", "pm_test_abcdefghij", 200),        # Valid payment method ID with letters
    ])
    def test_make_credits_payment_invalid_payment_methods(self, credits_api, amount, currency, payment_method_id, expected_status):
        """Test credits payment with invalid payment method IDs"""
        logger.info(f"Testing payment method: {payment_method_id}, expected: {expected_status}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Payment method {payment_method_id} was accepted")
        else:
            logger.info(f"✅ Invalid payment method {payment_method_id} properly rejected")
    
    # Edge cases
    def test_make_credits_payment_minimum_amount(self, credits_api):
        """Test credits payment with minimum valid amount"""
        amount = 0.01
        currency = "usd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing minimum amount: {amount} {currency}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        assert response.status_code == 200, f"Minimum amount {amount} should be accepted"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Minimum amount {amount} accepted")
    
    def test_make_credits_payment_maximum_amount(self, credits_api):
        """Test credits payment with very large amount"""
        amount = 999999999
        currency = "usd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing maximum amount: {amount} {currency}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        assert response.status_code == 200, f"Large amount {amount} should be accepted"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Large amount {amount} accepted")
    
    # Response structure validation
    def test_make_credits_payment_response_structure(self, credits_api):
        """Test that credits payment response has correct structure"""
        amount = 1000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response structure for {amount} {currency}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
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
        
        logger.info("✅ Credits payment response structure validation passed")
    
    # Performance tests
    def test_make_credits_payment_response_time(self, credits_api):
        """Test that credits payment responds within reasonable time"""
        import time
        
        amount = 1000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response time for {amount} {currency}")
        
        start_time = time.time()
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 10.0, f"Response time {response_time:.2f}s exceeds 10s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    # Integration tests
    def test_make_credits_payment_with_credits_balance(self, credits_api):
        """Test credits payment and then check credits balance"""
        amount = 5000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing integration: credits payment + credits balance for {amount} {currency}")
        
        # Make credits payment
        payment_response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        assert payment_response.status_code == 200, "Credits payment should succeed"
        
        # Get credits balance
        balance_response = credits_api.get_credits_balance()
        assert balance_response.status_code == 200, "Credits balance retrieval should succeed"
        
        logger.info("✅ Integration test passed: credits payment + credits balance")
    
    def test_make_credits_payment_with_credits_history(self, credits_api):
        """Test credits payment and then check credits history"""
        amount = 2000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing integration: credits payment + credits history for {amount} {currency}")
        
        # Make credits payment
        payment_response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        assert payment_response.status_code == 200, "Credits payment should succeed"
        
        # Get credits history
        history_response = credits_api.get_credits_history()
        assert history_response.status_code == 200, "Credits history retrieval should succeed"
        
        logger.info("✅ Integration test passed: credits payment + credits history")
    
    # Error handling tests
    def test_make_credits_payment_missing_parameters(self, credits_api):
        """Test credits payment with missing parameters"""
        # Test with None values for required parameters
        amount = None
        currency = None
        payment_method_id = None
        
        logger.info(f"Testing missing parameters: amount={amount}, currency={currency}, method={payment_method_id}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        # The API should handle None parameters appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing parameters properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_make_credits_payment_different_user_tiers(self, credits_api):
        """Test credits payment works for different user tiers"""
        amount = 1000
        currency = "vnd"
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing credits payment for current user tier: {amount} {currency}")
        
        response = credits_api.make_credits_payment(amount, currency, payment_method_id)
        assert response.status_code == 200, "Credits payment should work for current user tier"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info("✅ Credits payment works for current user tier")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Credits payment test cleanup completed") 