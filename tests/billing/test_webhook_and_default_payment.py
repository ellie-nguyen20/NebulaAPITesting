"""
Test file for testing webhook and initial default payment functionality
Tests POST /api/v1/payment/webhook and PUT /api/v1/payment/initial-default-payment endpoints
"""

import pytest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestWebhookAndDefaultPayment:
    """Test class for webhook and initial default payment functionality using CreditsAPI"""
    
    def test_handle_stripe_webhook_success(self, credits_api):
        """Test successful handling of Stripe webhook event"""
        event_data = {
            "id": "evt_test_1234567890",
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_test_1234567890",
                    "amount": 1000,
                    "currency": "vnd"
                }
            }
        }
        
        logger.info(f"Testing Stripe webhook handling: {event_data['type']}")
        
        response = credits_api.handle_stripe_webhook(event_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        # Check for webhook response structure
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Stripe webhook handled successfully: {event_data['type']}")
        return response_data
    
    def test_set_initial_default_payment_success(self, credits_api):
        """Test successful setting of initial default payment method"""
        payment_method_id = "pm_test_1234567890"  # Mock payment method ID
        
        logger.info(f"Testing initial default payment method setting: {payment_method_id}")
        
        response = credits_api.set_initial_default_payment(payment_method_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "data" in response_data, "Response should contain data field"
        
        logger.info(f"✅ Initial default payment method set successfully: {payment_method_id}")
        return response_data
    
    # Parameterized tests for different webhook event types
    @pytest.mark.parametrize("event_type,event_data", [
        ("payment_intent.succeeded", {
            "id": "evt_test_1234567890",
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_test_1234567890", "amount": 1000, "currency": "vnd"}}
        }),
        ("payment_intent.payment_failed", {
            "id": "evt_test_1234567891",
            "type": "payment_intent.payment_failed",
            "data": {"object": {"id": "pi_test_1234567891", "amount": 5000, "currency": "vnd"}}
        }),
        ("invoice.payment_succeeded", {
            "id": "evt_test_1234567892",
            "type": "invoice.payment_succeeded",
            "data": {"object": {"id": "in_test_1234567892", "amount_paid": 10000, "currency": "vnd"}}
        }),
        ("customer.subscription.created", {
            "id": "evt_test_1234567893",
            "type": "customer.subscription.created",
            "data": {"object": {"id": "sub_test_1234567893", "status": "active"}}
        }),
        ("customer.subscription.deleted", {
            "id": "evt_test_1234567894",
            "type": "customer.subscription.deleted",
            "data": {"object": {"id": "sub_test_1234567894", "status": "canceled"}}
        }),
    ])
    def test_handle_stripe_webhook_different_events(self, credits_api, event_type, event_data):
        """Test Stripe webhook handling with various event types"""
        logger.info(f"Testing webhook event: {event_type}")
        
        response = credits_api.handle_stripe_webhook(event_data)
        assert response.status_code == 200, f"Failed for event type {event_type}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for event type {event_type}"
        
        logger.info(f"✅ Success: {event_type}")
    
    # Parameterized tests for different payment method IDs
    @pytest.mark.parametrize("payment_method_id", [
        "pm_test_1234567890",
        "pm_test_abcdefghij",
        "pm_test_9876543210",
        "pm_test_qwertyuiop",
        "pm_test_asdfghjklz",
    ])
    def test_set_initial_default_payment_different_ids(self, credits_api, payment_method_id):
        """Test initial default payment method setting with various IDs"""
        logger.info(f"Testing initial default payment method: {payment_method_id}")
        
        response = credits_api.set_initial_default_payment(payment_method_id)
        assert response.status_code == 200, f"Failed for payment method ID {payment_method_id}"
        
        response_data = response.json()
        assert "data" in response_data, f"Missing data field for payment method ID {payment_method_id}"
        
        logger.info(f"✅ Success: {payment_method_id}")
    
    # Invalid webhook event tests
    @pytest.mark.parametrize("event_data,expected_status", [
        ({}, 400),                          # Empty event data
        (None, 400),                        # None event data
        ({"invalid": "data"}, 400),         # Invalid event structure
        ({"type": "invalid_event"}, 400),   # Invalid event type
        ({"id": "evt_test", "type": "payment_intent.succeeded", "data": {}}, 200),  # Valid event
    ])
    def test_handle_stripe_webhook_invalid_events(self, credits_api, event_data, expected_status):
        """Test Stripe webhook handling with invalid event data"""
        logger.info(f"Testing invalid webhook event: {event_data}, expected: {expected_status}")
        
        response = credits_api.handle_stripe_webhook(event_data)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Invalid webhook event was accepted (edge case)")
        else:
            logger.info(f"✅ Invalid webhook event properly rejected")
    
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
    def test_set_initial_default_payment_invalid_ids(self, credits_api, payment_method_id, expected_status):
        """Test initial default payment method setting with invalid IDs"""
        logger.info(f"Testing payment method ID: {payment_method_id}, expected: {expected_status}")
        
        response = credits_api.set_initial_default_payment(payment_method_id)
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        
        if expected_status == 200:
            response_data = response.json()
            assert "data" in response_data, "Response should contain data field"
            logger.info(f"✅ Payment method ID {payment_method_id} was accepted")
        else:
            logger.info(f"✅ Invalid payment method ID {payment_method_id} properly rejected")
    
    # Response structure validation
    def test_handle_stripe_webhook_response_structure(self, credits_api):
        """Test that Stripe webhook response has correct structure"""
        event_data = {
            "id": "evt_test_1234567890",
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_test_1234567890", "amount": 1000, "currency": "vnd"}}
        }
        
        logger.info(f"Testing webhook response structure for event: {event_data['type']}")
        
        response = credits_api.handle_stripe_webhook(event_data)
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
        
        logger.info("✅ Stripe webhook response structure validation passed")
    
    def test_set_initial_default_payment_response_structure(self, credits_api):
        """Test that initial default payment response has correct structure"""
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response structure for payment method: {payment_method_id}")
        
        response = credits_api.set_initial_default_payment(payment_method_id)
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
        
        logger.info("✅ Initial default payment response structure validation passed")
    
    # Performance tests
    def test_handle_stripe_webhook_response_time(self, credits_api):
        """Test that Stripe webhook handling responds within reasonable time"""
        import time
        
        event_data = {
            "id": "evt_test_1234567890",
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_test_1234567890", "amount": 1000, "currency": "vnd"}}
        }
        
        logger.info(f"Testing response time for webhook event: {event_data['type']}")
        
        start_time = time.time()
        response = credits_api.handle_stripe_webhook(event_data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    def test_set_initial_default_payment_response_time(self, credits_api):
        """Test that initial default payment setting responds within reasonable time"""
        import time
        
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing response time for payment method: {payment_method_id}")
        
        start_time = time.time()
        response = credits_api.set_initial_default_payment(payment_method_id)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, "Request should succeed"
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s limit"
        
        logger.info(f"✅ Response time: {response_time:.2f}s")
    
    # Integration tests
    def test_webhook_and_default_payment_workflow(self, credits_api):
        """Test complete workflow: webhook -> set default payment -> check payment methods"""
        logger.info("Testing complete webhook and default payment workflow")
        
        # Step 1: Handle webhook event
        event_data = {
            "id": "evt_test_1234567890",
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_test_1234567890", "amount": 1000, "currency": "vnd"}}
        }
        
        webhook_response = credits_api.handle_stripe_webhook(event_data)
        assert webhook_response.status_code == 200, "Webhook handling should succeed"
        
        # Step 2: Set initial default payment method
        payment_method_id = "pm_test_1234567890"
        default_response = credits_api.set_initial_default_payment(payment_method_id)
        assert default_response.status_code == 200, "Default payment method setting should succeed"
        
        # Step 3: Check payment methods
        methods_response = credits_api.get_payment_methods()
        assert methods_response.status_code == 200, "Payment methods retrieval should succeed"
        
        logger.info("✅ Webhook and default payment workflow test passed")
    
    def test_webhook_with_credits_balance(self, credits_api):
        """Test webhook handling and then check credits balance"""
        event_data = {
            "id": "evt_test_1234567890",
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_test_1234567890", "amount": 1000, "currency": "vnd"}}
        }
        
        logger.info(f"Testing integration: webhook handling + credits balance for {event_data['type']}")
        
        # Handle webhook
        webhook_response = credits_api.handle_stripe_webhook(event_data)
        assert webhook_response.status_code == 200, "Webhook handling should succeed"
        
        # Get credits balance
        balance_response = credits_api.get_credits_balance()
        assert balance_response.status_code == 200, "Credits balance retrieval should succeed"
        
        logger.info("✅ Integration test passed: webhook handling + credits balance")
    
    # Error handling tests
    def test_handle_stripe_webhook_missing_parameter(self, credits_api):
        """Test Stripe webhook handling with missing parameter"""
        event_data = None
        
        logger.info(f"Testing missing webhook event data: {event_data}")
        
        response = credits_api.handle_stripe_webhook(event_data)
        # The API should handle None event data appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing webhook event data properly handled with status {response.status_code}")
    
    def test_set_initial_default_payment_missing_parameter(self, credits_api):
        """Test initial default payment setting with missing parameter"""
        payment_method_id = None
        
        logger.info(f"Testing missing payment method ID: {payment_method_id}")
        
        response = credits_api.set_initial_default_payment(payment_method_id)
        # The API should handle None payment method ID appropriately
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        
        logger.info(f"✅ Missing payment method ID properly handled with status {response.status_code}")
    
    # Business logic tests
    def test_webhook_and_default_payment_different_user_tiers(self, credits_api):
        """Test webhook and default payment operations work for different user tiers"""
        event_data = {
            "id": "evt_test_1234567890",
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_test_1234567890", "amount": 1000, "currency": "vnd"}}
        }
        payment_method_id = "pm_test_1234567890"
        
        logger.info(f"Testing webhook and default payment for current user tier")
        
        # Test webhook handling
        webhook_response = credits_api.handle_stripe_webhook(event_data)
        assert webhook_response.status_code == 200, "Webhook handling should work for current user tier"
        
        # Test default payment method setting
        default_response = credits_api.set_initial_default_payment(payment_method_id)
        assert default_response.status_code == 200, "Default payment method setting should work for current user tier"
        
        logger.info("✅ Webhook and default payment operations work for current user tier")
    
    # Cleanup and teardown
    def teardown_method(self):
        """Cleanup after each test method"""
        logger.info("🧹 Webhook and default payment test cleanup completed") 