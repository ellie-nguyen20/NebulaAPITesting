"""
Test file for testing add credit/payment functionality
Comprehensive tests for create-checkout-session endpoint
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestAddCredit:
    """Test class for add credit/payment functionality using CreditsAPI"""
    
    def test_create_checkout_session_success(self, credits_api):
        """Test successful checkout session creation"""
        amount = 10
        currency = "usd"
        
        logger.info(f"Testing checkout session creation: {amount} {currency}")
        
        response = credits_api.create_checkout_session(amount, currency)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for payment API response structure
        assert "data" in response_data, "Response should contain data field"
        assert "redirect_url" in response_data["data"], "Response should contain data.redirect_url"
        
        logger.info(f"✅ Checkout session created successfully: {amount} {currency}")
        return response_data
    
    # Parameterized tests for different amounts and currencies
    @pytest.mark.parametrize("amount,currency", [
        (1, "usd"),
        (10, "usd"),
        (100, "usd"),
        (1000, "vnd"),
        (5000, "vnd"),
        (10000, "vnd"),
        (1, "eur"),
        (2, "eur"),
        (100, "jpy"),
    ])
    def test_create_checkout_session_different_amounts_currencies(self, credits_api, amount, currency):
        """Test checkout session creation with various amounts and currencies"""
        logger.info(f"Testing amount: {amount}, currency: {currency}")
        
        response = credits_api.create_checkout_session(amount, currency)
        assert response.status_code == 200, f"Failed for amount {amount} {currency}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for {amount} {currency}"
        assert "redirect_url" in response_data["data"], f"Missing redirect_url for {amount} {currency}"
        
        logger.info(f"✅ Success: {amount} {currency}")
    
    # Invalid amount tests
    @pytest.mark.parametrize("amount,currency,expected_status", [
        (0, "usd", 400),           # Zero amount
        (-1, "usd", 400),          # Negative amount
        (-100, "vnd", 400),        # Large negative amount
        ("invalid", "usd", 400),   # String amount
        (None, "usd", 400),        # None amount
        ("", "usd", 400),          # Empty string amount
        (0.01, "usd", 200),       # Small decimal amount (should work)
        (999999999, "usd", 200),  # Very large amount (should work)
    ])
    def test_create_checkout_session_invalid_amounts(self, credits_api, amount, currency, expected_status):
        """Test checkout session creation with invalid amounts"""
        logger.info(f"Testing invalid amount: {amount} {currency}, expected: {expected_status}")
        
        response = credits_api.create_checkout_session(amount, currency)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            assert "redirect_url" in response_data["data"], "Response should contain redirect_url"
            logger.info(f"✅ Invalid amount {amount} was accepted (edge case)")
        else:
            logger.info(f"✅ Invalid amount {amount} properly rejected")
    
    # Invalid currency tests
    @pytest.mark.parametrize("amount,currency,expected_status", [
        (1000, "invalid", 400),    # Invalid currency
        (1000, "", 400),           # Empty currency
        (1000, None, 400),         # None currency
        (1000, "123", 400),        # Numeric currency
        (1000, "USD", 400),        # Uppercase currency (if case-sensitive)
        (1000, "usd", 200),        # Valid lowercase
        (1000, "vnd", 200),        # Valid lowercase
        (1000, "eur", 200),        # Valid lowercase
    ])
    def test_create_checkout_session_invalid_currencies(self, credits_api, amount, currency, expected_status):
        """Test checkout session creation with invalid currencies"""
        logger.info(f"Testing currency: {currency}, expected: {expected_status}")
        
        response = credits_api.create_checkout_session(amount, currency)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            assert "redirect_url" in response_data["data"], "Response should contain redirect_url"
            logger.info(f"✅ Currency {currency} was accepted")
        else:
            logger.info(f"✅ Invalid currency {currency} properly rejected")
    
    # Edge cases
    def test_create_checkout_session_minimum_amount(self, credits_api):
        """Test checkout session with minimum valid amount"""
        amount = 0.01
        currency = "usd"
        
        logger.info(f"Testing minimum amount: {amount} {currency}")
        
        response = credits_api.create_checkout_session(amount, currency)
        assert response.status_code == 200, f"Minimum amount {amount} should be accepted"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        assert "redirect_url" in response_data["data"], "Response should contain redirect_url"
        
        logger.info(f"✅ Minimum amount {amount} accepted")
    
    def test_create_checkout_session_maximum_amount(self, credits_api):
        """Test checkout session with very large amount"""
        amount = 999999999
        currency = "usd"
        
        logger.info(f"Testing maximum amount: {amount} {currency}")
        
        response = credits_api.create_checkout_session(amount, currency)
        assert response.status_code == 200, f"Large amount {amount} should be accepted"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        assert "redirect_url" in response_data["data"], "Response should contain redirect_url"
        
        logger.info(f"✅ Large amount {amount} accepted")
    
    # Response structure validation
    def test_create_checkout_session_response_structure(self, credits_api):
        """Test that checkout session response has correct structure"""
        amount = 1000
        currency = "vnd"
        
        logger.info(f"Testing response structure for {amount} {currency}")
        
        response = credits_api.create_checkout_session(amount, currency)
        assert response.status_code == 200, "Request should succeed"
        
        response_data = response.json()
        
        # Check required fields
        assert "data" in response_data, "Response should contain 'data' field"
        assert "message" in response_data, "Response should contain 'message' field"
        assert "status" in response_data, "Response should contain 'status' field"
        
        # Check data sub-fields
        data = response_data["data"]
        assert "redirect_url" in data, "Data should contain 'redirect_url' field"
        
        # Check field types
        assert isinstance(response_data["message"], str), "Message should be string"
        assert isinstance(response_data["status"], str), "Status should be string"
        assert isinstance(data["redirect_url"], str), "Redirect URL should be string"
        
        # Check field values
        assert response_data["status"] == "success", "Status should be 'success'"
        assert "checkout.stripe.com" in data["redirect_url"], "Redirect URL should contain Stripe domain"
        
        logger.info("✅ Response structure validation passed")
    
    # Performance tests
    def test_create_checkout_session_response_time(self, credits_api):
        """Test that checkout session creation responds within reasonable time"""
        import time
        
        amount = 1000
        currency = "vnd"
        
        logger.info(f"Testing response time for {amount} {currency}")
        
        start_time = time.time()
        response = credits_api.create_checkout_session(amount, currency)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    # Integration tests
    def test_create_checkout_session_with_credits_balance(self, credits_api):
        """Test checkout session creation and then check credits balance"""
        amount = 5000
        currency = "vnd"
        
        logger.info(f"Testing integration: checkout session + credits balance for {amount} {currency}")
        
        # Create checkout session
        checkout_response = credits_api.create_checkout_session(amount, currency)
        assert checkout_response.status_code == 200, "Checkout session creation should succeed"
        
        # Get credits balance
        balance_response = credits_api.get_credits_balance()
        assert balance_response.status_code == 200, "Credits balance retrieval should succeed"
        
        logger.info("✅ Integration test passed: checkout session + credits balance")
    
    def test_create_checkout_session_with_credits_history(self, credits_api):
        """Test checkout session creation and then check credits history"""
        amount = 2000
        currency = "vnd"
        
        logger.info(f"Testing integration: checkout session + credits history for {amount} {currency}")
        
        # Create checkout session
        checkout_response = credits_api.create_checkout_session(amount, currency)
        assert checkout_response.status_code == 200, "Checkout session creation should succeed"
        
        # Get credits history
        history_response = credits_api.get_credits_history()
        assert history_response.status_code == 200, "Credits history retrieval should succeed"
        
        logger.info("✅ Integration test passed: checkout session + credits history")
    
    # Error handling tests
    def test_create_checkout_session_missing_amount(self, credits_api):
        """Test checkout session creation with missing amount parameter"""
        # This test would require modifying the API client to test missing parameters
        # For now, we'll test with None amount which should be handled by the API
        amount = None
        currency = "usd"
        
        logger.info(f"Testing missing amount parameter: {amount} {currency}")
        
        response = credits_api.create_checkout_session(amount, currency)
        # The API should handle None amount appropriately
        # This could return 400 (Bad Request) or 422 (Unprocessable Entity)
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing amount properly handled with status {response.status_code}")
    
    def test_create_checkout_session_missing_currency(self, credits_api):
        """Test checkout session creation with missing currency parameter"""
        # This test would require modifying the API client to test missing parameters
        # For now, we'll test with None currency which should be handled by the API
        amount = 1000
        currency = None
        
        logger.info(f"Testing missing currency parameter: {amount} {currency}")
        
        response = credits_api.create_checkout_session(amount, currency)
        # The API should handle None currency appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing currency properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_create_checkout_session_different_user_tiers(self, credits_api):
        """Test checkout session creation works for different user tiers"""
        # This test assumes different user tiers might have different behavior
        # For now, we'll test with the current user tier
        amount = 1000
        currency = "vnd"
        
        logger.info(f"Testing checkout session for current user tier: {amount} {currency}")
        
        response = credits_api.create_checkout_session(amount, currency)
        assert response.status_code == 200, "Checkout session should work for current user tier"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        assert "redirect_url" in response_data["data"], "Response should contain redirect_url"
        
        logger.info("✅ Checkout session works for current user tier")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Test cleanup completed")
    

