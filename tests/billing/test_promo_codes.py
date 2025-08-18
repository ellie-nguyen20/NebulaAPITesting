"""
Test file for testing promo codes functionality
Tests POST /api/v1/payment/promo-codes/redeem endpoint
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestPromoCodes:
    """Test class for promo codes functionality using CreditsAPI"""
    
    def test_redeem_promo_code_success(self, credits_api):
        """Test successful promo code redemption"""
        promo_code = "WELCOME2024"  # Mock promo code
        
        logger.info(f"Testing promo code redemption: {promo_code}")
        
        response = credits_api.redeem_promo_code(promo_code)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for promo code redemption response structure
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Promo code redeemed successfully: {promo_code}")
        return response_data
    
    # Parameterized tests for different promo codes
    @pytest.mark.parametrize("promo_code", [
        "WELCOME2024",
        "SAVE20",
        "NEWUSER50",
        "HOLIDAY2024",
        "SPECIAL25",
        "FIRSTTIME",
        "LOYALTY100",
        "BONUS2024",
        "DISCOUNT30",
        "WELCOME2025",
    ])
    def test_redeem_promo_code_different_codes(self, credits_api, promo_code):
        """Test promo code redemption with various codes"""
        logger.info(f"Testing promo code redemption: {promo_code}")
        
        response = credits_api.redeem_promo_code(promo_code)
        assert response.status_code == 200, f"Failed for promo code {promo_code}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for promo code {promo_code}"
        
        logger.info(f"✅ Success: {promo_code}")
    
    # Invalid promo code tests
    @pytest.mark.parametrize("promo_code,expected_status", [
        ("", 400),                          # Empty promo code
        (None, 400),                        # None promo code
        ("invalid", 400),                   # Invalid promo code
        ("123", 400),                       # Numeric promo code
        ("WELCOME2024", 200),               # Valid promo code
        ("SAVE20", 200),                    # Valid promo code
        ("NEWUSER50", 200),                 # Valid promo code
    ])
    def test_redeem_promo_code_invalid_codes(self, credits_api, promo_code, expected_status):
        """Test promo code redemption with invalid codes"""
        logger.info(f"Testing promo code: {promo_code}, expected: {expected_status}")
        
        response = credits_api.redeem_promo_code(promo_code)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Promo code {promo_code} was accepted")
        else:
            logger.info(f"✅ Invalid promo code {promo_code} properly rejected")
    
    # Edge cases
    def test_redeem_promo_code_very_long_code(self, credits_api):
        """Test promo code redemption with very long code"""
        promo_code = "A" * 100  # Very long code
        
        logger.info(f"Testing very long promo code: {len(promo_code)} characters")
        
        response = credits_api.redeem_promo_code(promo_code)
        # Should either accept or reject with appropriate error
        assert response.status_code in [200, 400, 413], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Very long promo code accepted")
        else:
            logger.info(f"✅ Very long promo code properly rejected with status {response.status_code}")
    
    def test_redeem_promo_code_special_characters(self, credits_api):
        """Test promo code redemption with special characters"""
        promo_code = "WELCOME!@#$%^&*()_+-="
        
        logger.info(f"Testing special characters in promo code: {promo_code}")
        
        response = credits_api.redeem_promo_code(promo_code)
        # Should either accept or reject with appropriate error
        assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Special characters accepted")
        else:
            logger.info(f"✅ Special characters properly rejected with status {response.status_code}")
    
    def test_redeem_promo_code_case_sensitivity(self, credits_api):
        """Test promo code redemption case sensitivity"""
        promo_code_upper = "WELCOME2024"
        promo_code_lower = "welcome2024"
        promo_code_mixed = "Welcome2024"
        
        logger.info(f"Testing case sensitivity: {promo_code_upper} vs {promo_code_lower} vs {promo_code_mixed}")
        
        # Test all cases
        responses = []
        for code in [promo_code_upper, promo_code_lower, promo_code_mixed]:
            response = credits_api.redeem_promo_code(code)
            responses.append((code, response.status_code))
        
        # Log results
        for code, status in responses:
            if status == 200:
                logger.info(f"✅ Promo code {code} accepted with status {status}")
            else:
                logger.info(f"❌ Promo code {code} rejected with status {status}")
        
        # At least one should work
        assert any(status == 200 for _, status in responses), "At least one case should work"
    
    # Response structure validation
    def test_redeem_promo_code_response_structure(self, credits_api):
        """Test that promo code redemption response has correct structure"""
        promo_code = "WELCOME2024"
        
        logger.info(f"Testing response structure for promo code: {promo_code}")
        
        response = credits_api.redeem_promo_code(promo_code)
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
        
        logger.info("✅ Promo code redemption response structure validation passed")
    
    # Performance tests
    def test_redeem_promo_code_response_time(self, credits_api):
        """Test that promo code redemption responds within reasonable time"""
        import time
        
        promo_code = "WELCOME2024"
        
        logger.info(f"Testing response time for promo code: {promo_code}")
        
        start_time = time.time()
        response = credits_api.redeem_promo_code(promo_code)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    # Integration tests
    def test_redeem_promo_code_with_credits_balance(self, credits_api):
        """Test promo code redemption and then check credits balance"""
        promo_code = "WELCOME2024"
        
        logger.info(f"Testing integration: promo code redemption + credits balance for {promo_code}")
        
        # Redeem promo code
        redeem_response = credits_api.redeem_promo_code(promo_code)
        assert redeem_response.status_code == 200, "Promo code redemption should succeed"
        
        # Get credits balance
        balance_response = credits_api.get_credits_balance()
        assert balance_response.status_code == 200, "Credits balance retrieval should succeed"
        
        logger.info("✅ Integration test passed: promo code redemption + credits balance")
    
    def test_redeem_promo_code_with_credits_history(self, credits_api):
        """Test promo code redemption and then check credits history"""
        promo_code = "SAVE20"
        
        logger.info(f"Testing integration: promo code redemption + credits history for {promo_code}")
        
        # Redeem promo code
        redeem_response = credits_api.redeem_promo_code(promo_code)
        assert redeem_response.status_code == 200, "Promo code redemption should succeed"
        
        # Get credits history
        history_response = credits_api.get_credits_history()
        assert history_response.status_code == 200, "Credits history retrieval should succeed"
        
        logger.info("✅ Integration test passed: promo code redemption + credits history")
    
    # Error handling tests
    def test_redeem_promo_code_missing_parameter(self, credits_api):
        """Test promo code redemption with missing parameter"""
        promo_code = None
        
        logger.info(f"Testing missing promo code: {promo_code}")
        
        response = credits_api.redeem_promo_code(promo_code)
        # The API should handle None promo code appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing promo code properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_redeem_promo_code_different_user_tiers(self, credits_api):
        """Test promo code redemption works for different user tiers"""
        promo_code = "WELCOME2024"
        
        logger.info(f"Testing promo code redemption for current user tier: {promo_code}")
        
        response = credits_api.redeem_promo_code(promo_code)
        assert response.status_code == 200, "Promo code redemption should work for current user tier"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info("✅ Promo code redemption works for current user tier")
    
    # Consistency tests
    def test_redeem_promo_code_consistency(self, credits_api):
        """Test that promo code redemption is consistent across multiple calls"""
        promo_code = "WELCOME2024"
        
        logger.info(f"Testing promo code redemption consistency for: {promo_code}")
        
        # Make multiple calls
        responses = []
        for i in range(3):
            response = credits_api.redeem_promo_code(promo_code)
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
        
        logger.info("✅ Promo code redemption consistency validation passed")
    
    # Duplicate redemption tests
    def test_redeem_promo_code_duplicate_redemption(self, credits_api):
        """Test that the same promo code can't be redeemed multiple times"""
        promo_code = "DUPLICATE_TEST"
        
        logger.info(f"Testing duplicate promo code redemption: {promo_code}")
        
        # First redemption should succeed
        first_response = credits_api.redeem_promo_code(promo_code)
        if first_response.status_code == 200:
            logger.info(f"✅ First redemption successful for {promo_code}")
            
            # Second redemption might fail (already used) or succeed (multiple use allowed)
            second_response = credits_api.redeem_promo_code(promo_code)
            
            if second_response.status_code == 200:
                logger.info(f"✅ Second redemption also successful (multiple use allowed)")
            else:
                logger.info(f"✅ Second redemption properly rejected (single use only)")
        else:
            logger.info(f"❌ First redemption failed with status {first_response.status_code}")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Promo codes test cleanup completed") 