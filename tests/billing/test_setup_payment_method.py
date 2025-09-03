import pytest

def test_setup_payment_method(credits_api):
    """Test setting up a payment method"""
    response = credits_api.set_up_payment_method("pm_1QZ882FZ882FZ882FZ882FZ8")
   
    print("hellooooooooooooooo")
    print(response.json())
    # assert response.ok, "Failed to set up payment method"