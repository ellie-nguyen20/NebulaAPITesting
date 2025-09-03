from .base_api import BaseAPIClient

class CreditsAPI(BaseAPIClient):
    """Credits API client for managing credits operations."""
    # Create Checkout Session
    def create_checkout_session(self, amount):
        """Create checkout session for payment."""
        payload = {"amount": amount}
        return self.post("/payment/create-checkout-session", data=payload)
    
    # Add Credit
    def add_credit(self, amount, currency):
        """Add credits to account (alias for create_checkout_session)."""
        return self.create_checkout_session(amount, currency)
    
    # Get Credits Balance
    def get_credits_balance(self):
        """Get current credits balance."""
        return self.get("/credits/balance")
    
    # Get Credits History
    def get_credits_history(self):
        """Get credits transaction history."""
        return self.get("/credits/history")
    
    # Payment Options
    def get_payment_options(self):
        """List payment options."""
        return self.get("/payment/options")
    
    # Credits Payment
    def make_credits_payment(self, amount, currency, payment_method_id):
        """Make credits payment."""
        payload = {
            "amount": amount,
            "currency": currency,
            "payment_method_id": payment_method_id
        }
        return self.post("/payment/payment", data=payload)
    
    # Setup Intent
    def create_setup_intent(self, payment_method_id):
        """Create setup intent."""
        payload = {"payment_method_id": payment_method_id}
        return self.post("/payment/setup-intent", data=payload)
    
    # Auto Pay
    def get_auto_pay_setting(self):
        """Get auto pay setting."""
        return self.get("/payment/auto-pay")
    
    def update_auto_pay_setting(self, enabled, payment_method_id=None):
        """Update auto pay setting."""
        payload = {"enabled": enabled}
        if payment_method_id:
            payload["payment_method_id"] = payment_method_id
        return self.put("/payment/auto-pay", data=payload)
    
    # Payment Intent
    def create_payment_intent(self, amount, currency, payment_method_id):
        """Create payment intent."""
        payload = {
            "amount": amount,
            "currency": currency,
            "payment_method_id": payment_method_id
        }
        return self.post("/payment/payment-intent", data=payload)
    
    def confirm_payment_intent(self, payment_intent_id):
        """Confirm payment intent."""
        payload = {"payment_intent_id": payment_intent_id}
        return self.post("/payment/payment-intent-confirmation", data=payload)
    
    # Default Payment Method
    def set_initial_default_payment(self, payment_method_id):
        """Check and set initial default payment method."""
        payload = {"payment_method_id": payment_method_id}
        return self.put("/payment/initial-default-payment", data=payload)
    
    # Payment Methods
    def get_payment_methods(self):
        """Get payment methods by user ID."""
        return self.get("/payment/payment-methods")
    
    def update_default_payment_method(self, payment_method_id):
        """Update default payment method."""
        payload = {"payment_method_id": payment_method_id}
        return self.put("/payment/payment-methods/default", data=payload)
    
    # Webhook
    def handle_stripe_webhook(self, event_data):
        """Handle Stripe webhook event."""
        return self.post("/payment/webhook", data=event_data)
    
    # Validation
    def validate_payment_method(self, payment_method_id):
        """Validate payment method endpoint."""
        payload = {"payment_method_id": payment_method_id}
        return self.post("/payment/validate", data=payload)
    
    # Promo Codes
    def redeem_promo_code(self, promo_code):
        """Redeem promo code."""
        payload = {"promo_code": promo_code}
        return self.post("/payment/promo-codes/redeem", data=payload)
    
    # Delete Payment Method
    def delete_stripe_method(self, payment_method_id):
        """Delete Stripe payment method."""
        payload = {"payment_method_id": payment_method_id}
        return self.post("/payment/delete", data=payload)

    # Set up Payment Method
    def set_up_payment_method(self, payment_method_id):
        """Set up payment method."""
        payload = {"payment_method_id": payment_method_id}
        return self.post("/payment/setup_payment_method", data=payload)