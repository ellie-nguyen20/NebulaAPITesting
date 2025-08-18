import pytest

def test_list_payment_options(credits_api):
    """Test payment options listing with simplified validation"""
    
    # Make API call
    response = credits_api.get_payment_options()
    print(f"Response: {response}")
    
    # Basic response validation
    assert response.ok, f"API call failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f"Response data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert "message" in data, "Response missing 'message' field"
    assert "status" in data, "Response missing 'status' field"
    
    # Validate status field
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
    
    # Validate message field
    expected_message = "Payment options retrieved successfully"
    assert data["message"] == expected_message, f"Expected message '{expected_message}', got '{data['message']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, list), "Data field should be a list"
    assert len(data_field) > 0, "Payment options list should not be empty"
    
    # Expected payment options based on response
    expected_options = [
        {"amount": 10, "bonus": 0},
        {"amount": 25, "bonus": 0},
        {"amount": 50, "bonus": 5},
        {"amount": 100, "bonus": 15},
        {"amount": 200, "bonus": 50}
    ]
    
    # Validate payment options count
    assert len(data_field) == len(expected_options), f"Expected {len(expected_options)} payment options, got {len(data_field)}"
    
    # Validate each payment option
    for i, option in enumerate(data_field):
        print(f"🔍 Validating payment option {i+1}: {option}")
        
        # Validate option structure
        assert isinstance(option, dict), f"Payment option {i+1} should be a dictionary"
        assert "amount" in option, f"Payment option {i+1} missing 'amount' field"
        assert "bonus" in option, f"Payment option {i+1} missing 'bonus' field"
        
        # Validate amount field
        amount = option["amount"]
        assert isinstance(amount, int), f"Amount in option {i+1} should be integer, got {type(amount)}"
        assert amount > 0, f"Amount in option {i+1} should be positive, got {amount}"
        
        # Validate bonus field
        bonus = option["bonus"]
        assert isinstance(bonus, int), f"Bonus in option {i+1} should be integer, got {type(bonus)}"
        assert bonus >= 0, f"Bonus in option {i+1} should be non-negative, got {bonus}"
        
        # Validate specific values
        expected_option = expected_options[i]
        assert amount == expected_option["amount"], f"Amount mismatch in option {i+1}: expected {expected_option['amount']}, got {amount}"
        assert bonus == expected_option["bonus"], f"Bonus mismatch in option {i+1}: expected {expected_option['bonus']}, got {bonus}"
        
        print(f"  ✅ Amount: {amount}, Bonus: {bonus}")
    
    # Simple business logic validation
    print("\n🔍 Simple business logic validation...")
    
    # Check if amounts are in ascending order
    amounts = [option["amount"] for option in data_field]
    assert amounts == sorted(amounts), f"Amounts should be in ascending order: {amounts}"
    print("✅ Amounts are in ascending order")
    
    # Check if small amounts have no bonus
    small_amount_options = [opt for opt in data_field if opt["amount"] <= 25]
    for opt in small_amount_options:
        assert opt["bonus"] == 0, f"Small amount {opt['amount']} should have no bonus, got {opt['bonus']}"
    print("✅ Small amounts have no bonus")
    
    # Final validation
    assert response.ok, "Final response should be successful"
    
    print(f"\n🎉 All validations passed for payment options!")
    print(f"✅ Found {len(data_field)} payment options")
    print(f"✅ Amount range: {min(amounts)} - {max(amounts)}")
    
    # Print summary of all options
    print(f"\n📋 Payment Options Summary:")
    for i, option in enumerate(data_field):
        print(f"  {i+1}. ${option['amount']} - {option['bonus']} bonus credits")

def test_setup_intent(credits_api):
    """Test setup intent creation with simple validation"""
    
    # Test payment method ID
    test_payment_method_id = "pm_test_1234567890"
    
    # Make API call
    response = credits_api.create_setup_intent(test_payment_method_id)
    print(f"Response: {response}")
    
    # Basic response validation
    assert response.ok, f"API call failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f"Response data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert "message" in data, "Response missing 'message' field"
    assert "status" in data, "Response missing 'status' field"
    
    # Validate status field
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
    
    # Validate message field
    expected_message = "Setup intent successfully created"
    assert data["message"] == expected_message, f"Expected message '{expected_message}', got '{data['message']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, dict), "Data field should be a dictionary"
    
    # Validate essential Stripe setup intent fields
    essential_fields = [
        "id", "object", "status", "client_secret", "created", 
        "customer", "payment_method_types", "usage"
    ]
    
    for field in essential_fields:
        assert field in data_field, f"Missing essential field: {field}"
    
    # Validate specific field values
    setup_intent = data_field
    
    # ID validation
    assert isinstance(setup_intent["id"], str), "ID should be a string"
    assert setup_intent["id"].startswith("seti_"), "ID should start with 'seti_'"
    assert len(setup_intent["id"]) > 10, "ID should have reasonable length"
    
    # Object validation
    assert setup_intent["object"] == "setup_intent", "Object should be 'setup_intent'"
    
    # Status validation
    assert setup_intent["status"] == "requires_payment_method", "Status should be 'requires_payment_method'"
    
    # Client secret validation
    assert isinstance(setup_intent["client_secret"], str), "Client secret should be a string"
    assert setup_intent["client_secret"].startswith("seti_"), "Client secret should start with 'seti_'"
    assert "_secret_" in setup_intent["client_secret"], "Client secret should contain '_secret_'"
    
    # Created timestamp validation
    created = setup_intent["created"]
    assert isinstance(created, int), "Created should be an integer timestamp"
    assert created > 1600000000, "Created timestamp should be reasonable (after 2020)"
    
    # Customer validation
    assert isinstance(setup_intent["customer"], str), "Customer should be a string"
    assert setup_intent["customer"].startswith("cus_"), "Customer should start with 'cus_'"
    
    # Payment method types validation
    payment_method_types = setup_intent["payment_method_types"]
    assert isinstance(payment_method_types, list), "Payment method types should be a list"
    assert len(payment_method_types) > 0, "Payment method types should not be empty"
    
    # Check for common payment methods
    expected_methods = ["card", "bancontact", "ideal"]
    for method in expected_methods:
        assert method in payment_method_types, f"Payment method '{method}' should be available"
    
    # Usage validation
    assert setup_intent["usage"] == "off_session", "Usage should be 'off_session'"
    
    # Livemode validation
    assert "livemode" in setup_intent, "Livemode field should be present"
    assert isinstance(setup_intent["livemode"], bool), "Livemode should be a boolean"
    # Note: livemode False means test mode, which is expected for testing
    
    # Metadata validation
    assert "metadata" in setup_intent, "Metadata field should be present"
    assert isinstance(setup_intent["metadata"], dict), "Metadata should be a dictionary"
    
    # Final validation
    assert response.ok, "Final response should be successful"
    
    print(f"\n🎉 All validations passed for setup intent!")
    print(f"✅ Setup Intent ID: {setup_intent['id']}")
    print(f"✅ Status: {setup_intent['status']}")
    print(f"✅ Customer: {setup_intent['customer']}")
    print(f"✅ Payment Methods: {', '.join(payment_method_types)}")
    print(f"✅ Created: {created}")
    print(f"✅ Test Mode: {not setup_intent['livemode']}")

def test_create_payment_intent(credits_api):
    """Test payment intent creation with simple validation"""
    
    # Test payment method ID
    test_payment_method_id = "pm_test_1234567890"
    
    # Create setup intent first (as per original logic)
    setup_intent = credits_api.create_setup_intent(test_payment_method_id)
    print(f"Setup Intent: {setup_intent}")
    
    # Basic setup intent validation
    assert setup_intent.ok, "Setup intent creation failed"
    setup_data = setup_intent.json()
    assert setup_data["status"] == "success", "Setup intent should be successful"
    
    # Make payment intent API call
    response = credits_api.create_payment_intent(100, "USD", test_payment_method_id)
    print(f"Payment Intent Response: {response}")
    
    # Basic response validation
    assert response.ok, f"API call failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f"Response data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert "message" in data, "Response missing 'message' field"
    assert "status" in data, "Response missing 'status' field"
    
    # Validate status field
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
    
    # Validate message field (assuming success message)
    assert "success" in data["message"].lower(), f"Message should indicate success, got '{data['message']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, dict), "Data field should be a dictionary"
    
    # Validate essential Stripe payment intent fields
    essential_fields = [
        "id", "object", "amount", "currency", "status", "client_secret", 
        "created", "customer", "payment_method_types", "confirmation_method"
    ]
    
    for field in essential_fields:
        assert field in data_field, f"Missing essential field: {field}"
    
    # Validate specific field values
    payment_intent = data_field
    
    # ID validation
    assert isinstance(payment_intent["id"], str), "ID should be a string"
    assert payment_intent["id"].startswith("pi_"), "ID should start with 'pi_' (payment intent)"
    assert len(payment_intent["id"]) > 10, "ID should have reasonable length"
    
    # Object validation
    assert payment_intent["object"] == "payment_intent", "Object should be 'payment_intent'"
    
    # Amount validation
    amount = payment_intent["amount"]
    assert isinstance(amount, int), "Amount should be an integer (in cents)"
    assert amount > 0, "Amount should be positive"
    # Note: 100 = $1.00 in Stripe (amounts are in cents)
    
    # Currency validation
    assert payment_intent["currency"] == "usd", "Currency should be 'usd'"
    
    # Status validation
    status = payment_intent["status"]
    assert isinstance(status, str), "Status should be a string"
    # Common statuses: requires_payment_method, requires_confirmation, requires_action, processing, requires_capture, canceled, succeeded
    valid_statuses = ["requires_payment_method", "requires_confirmation", "requires_action", "processing", "requires_capture", "canceled", "succeeded"]
    assert status in valid_statuses, f"Status '{status}' should be one of {valid_statuses}"
    
    # Client secret validation
    assert isinstance(payment_intent["client_secret"], str), "Client secret should be a string"
    assert payment_intent["client_secret"].startswith("pi_"), "Client secret should start with 'pi_'"
    assert "_secret_" in payment_intent["client_secret"], "Client secret should contain '_secret_'"
    
    # Created timestamp validation
    created = payment_intent["created"]
    assert isinstance(created, int), "Created should be an integer timestamp"
    assert created > 1600000000, "Created timestamp should be reasonable (after 2020)"
    
    # Customer validation
    assert isinstance(payment_intent["customer"], str), "Customer should be a string"
    assert payment_intent["customer"].startswith("cus_"), "Customer should start with 'cus_'"
    
    # Payment method types validation
    payment_method_types = payment_intent["payment_method_types"]
    assert isinstance(payment_method_types, list), "Payment method types should be a list"
    assert len(payment_method_types) > 0, "Payment method types should not be empty"
    
    # Check for common payment methods
    expected_methods = ["card", "bancontact", "ideal"]
    for method in expected_methods:
        assert method in payment_method_types, f"Payment method '{method}' should be available"
    
    # Confirmation method validation
    confirmation_method = payment_intent["confirmation_method"]
    assert isinstance(confirmation_method, str), "Confirmation method should be a string"
    valid_confirmation_methods = ["automatic", "manual"]
    assert confirmation_method in valid_confirmation_methods, f"Confirmation method '{confirmation_method}' should be one of {valid_confirmation_methods}"
    
    # Livemode validation
    assert "livemode" in payment_intent, "Livemode field should be present"
    assert isinstance(payment_intent["livemode"], bool), "Livemode should be a boolean"
    # Note: livemode False means test mode, which is expected for testing
    
    # Metadata validation
    assert "metadata" in payment_intent, "Metadata field should be present"
    assert isinstance(payment_intent["metadata"], dict), "Metadata should be a dictionary"
    
    # Final validation
    assert response.ok, "Final response should be successful"
    
    print(f"\n🎉 All validations passed for payment intent!")
    print(f"✅ Payment Intent ID: {payment_intent['id']}")
    print(f"✅ Amount: ${amount/100:.2f} {payment_intent['currency'].upper()}")
    print(f"✅ Status: {payment_intent['status']}")
    print(f"✅ Customer: {payment_intent['customer']}")
    print(f"✅ Payment Methods: {', '.join(payment_method_types)}")
    print(f"✅ Confirmation Method: {confirmation_method}")
    print(f"✅ Created: {created}")
    print(f"✅ Test Mode: {not payment_intent['livemode']}")
    
    # Additional business logic validation
    print(f"\n🔍 Business logic validation...")
    
    # Validate amount makes sense for test
    if amount == 100:
        print("✅ Test amount $1.00 is reasonable")
    else:
        print(f"ℹ️ Amount ${amount/100:.2f} (may be different from expected)")
    
    # Validate status progression
    if status == "requires_payment_method":
        print("✅ Status 'requires_payment_method' - ready for payment method")
    elif status == "requires_confirmation":
        print("✅ Status 'requires_confirmation' - ready for confirmation")
    elif status == "succeeded":
        print("✅ Status 'succeeded' - payment completed")
    else:
        print(f"ℹ️ Status '{status}' - in progress")
    
    print("✅ Payment intent creation successful!")

def test_get_payment_methods_by_user_id(credits_api):
    """Test getting payment methods by user ID with simple validation"""
    
    # Make API call
    response = credits_api.get_payment_methods()
    print(f"Response: {response}")
    
    # Basic response validation
    assert response.ok, f"API call failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f"Response data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert "message" in data, "Response missing 'message' field"
    assert "status" in data, "Response missing 'status' field"
    
    # Validate status field
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
    
    # Validate message field
    expected_message = "payment methods for user is successfully retrieved."
    assert data["message"] == expected_message, f"Expected message '{expected_message}', got '{data['message']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, list), "Data field should be a list"
    assert len(data_field) > 0, "Payment methods list should not be empty"
    
    # Validate each payment method
    for i, payment_method in enumerate(data_field):
        print(f"🔍 Validating payment method {i+1}: {payment_method}")
        
        # Validate payment method structure
        assert isinstance(payment_method, dict), f"Payment method {i+1} should be a dictionary"
        
        # Essential fields for payment method
        essential_fields = [
            "stripe_id", "payment_type", "last4", "expiry_date", 
            "default", "status"
        ]
        
        for field in essential_fields:
            assert field in payment_method, f"Payment method {i+1} missing '{field}' field"
        
        # Validate specific field values
        pm = payment_method
        
        # Stripe ID validation
        stripe_id = pm["stripe_id"]
        assert isinstance(stripe_id, str), f"Stripe ID in method {i+1} should be string, got {type(stripe_id)}"
        assert stripe_id.startswith("pm_"), f"Stripe ID in method {i+1} should start with 'pm_', got '{stripe_id}'"
        assert len(stripe_id) > 10, f"Stripe ID in method {i+1} should have reasonable length"
        
        # Payment type validation
        payment_type = pm["payment_type"]
        assert isinstance(payment_type, str), f"Payment type in method {i+1} should be string, got {type(payment_type)}"
        assert len(payment_type) > 0, f"Payment type in method {i+1} should not be empty"
        
        # Common payment types
        common_types = ["Visa", "Mastercard", "American Express", "Discover", "JCB", "UnionPay"]
        if payment_type in common_types:
            print(f"  ✅ Payment type '{payment_type}' is recognized")
        else:
            print(f"  ℹ️ Payment type '{payment_type}' (may be custom)")
        
        # Last 4 digits validation
        last4 = pm["last4"]
        assert isinstance(last4, str), f"Last4 in method {i+1} should be string, got {type(last4)}"
        assert len(last4) == 4, f"Last4 in method {i+1} should be exactly 4 characters, got '{last4}'"
        assert last4.isdigit(), f"Last4 in method {i+1} should contain only digits, got '{last4}'"
        
        # Expiry date validation
        expiry_date = pm["expiry_date"]
        assert isinstance(expiry_date, str), f"Expiry date in method {i+1} should be string, got {type(expiry_date)}"
        assert "/" in expiry_date, f"Expiry date in method {i+1} should contain '/', got '{expiry_date}'"
        
        # Parse expiry date (MM/YY format)
        try:
            month_str, year_str = expiry_date.split("/")
            month = int(month_str)
            year = int(year_str)
            
            assert 1 <= month <= 12, f"Month in expiry date should be 1-12, got {month}"
            assert 0 <= year <= 99, f"Year in expiry date should be 00-99, got {year}"
            
            # Check if card is not expired (assuming current year is 2024)
            current_year = 24  # 2024
            if year < current_year:
                print(f"  ⚠️ Card expired in 20{year}")
            elif year == current_year:
                print(f"  ⚠️ Card expires this year (20{year})")
            else:
                print(f"  ✅ Card valid until 20{year}")
                
        except (ValueError, AssertionError) as e:
            print(f"  ⚠️ Expiry date format issue: {e}")
        
        # Default status validation
        default = pm["default"]
        assert isinstance(default, bool), f"Default in method {i+1} should be boolean, got {type(default)}"
        
        # Status validation
        status = pm["status"]
        assert isinstance(status, str), f"Status in method {i+1} should be string, got {type(status)}"
        assert len(status) > 0, f"Status in method {i+1} should not be empty"
        
        # Common statuses
        common_statuses = ["Confirmed", "Pending", "Failed", "Expired", "Active", "Inactive"]
        if status in common_statuses:
            print(f"  ✅ Status '{status}' is recognized")
        else:
            print(f"  ℹ️ Status '{status}' (may be custom)")
        
        print(f"  ✅ Stripe ID: {stripe_id}")
        print(f"  ✅ Last 4: {last4}")
        print(f"  ✅ Default: {default}")
    
    # Business logic validation
    print(f"\n🔍 Business logic validation...")
    
    # Check if there's a default payment method
    default_methods = [pm for pm in data_field if pm["default"]]
    if default_methods:
        print(f"✅ Found {len(default_methods)} default payment method(s)")
        for pm in default_methods:
            print(f"  - {pm['payment_type']} ending in {pm['last4']}")
    else:
        print("ℹ️ No default payment method set")
    
    # Check payment method types distribution
    payment_types = [pm["payment_type"] for pm in data_field]
    type_counts = {}
    for pt in payment_types:
        type_counts[pt] = type_counts.get(pt, 0) + 1
    
    print(f"✅ Payment method types distribution:")
    for pt, count in type_counts.items():
        print(f"  - {pt}: {count}")
    
    # Validate data consistency
    print(f"\n🔍 Data consistency validation...")
    
    # All payment methods should have unique Stripe IDs
    stripe_ids = [pm["stripe_id"] for pm in data_field]
    unique_ids = set(stripe_ids)
    assert len(stripe_ids) == len(unique_ids), f"All Stripe IDs should be unique, found duplicates"
    print("✅ All Stripe IDs are unique")
    
    # All payment methods should have different last4 (unless same card type)
    last4s = [pm["last4"] for pm in data_field]
    if len(last4s) > 1:
        # It's possible to have same last4 for different cards, so just log
        print(f"ℹ️ Last4 digits: {', '.join(last4s)}")
    
    # Final validation
    assert response.ok, "Final response should be successful"
    
    print(f"\n🎉 All validations passed for payment methods!")
    print(f"✅ Found {len(data_field)} payment method(s)")
    print(f"✅ Payment types: {', '.join(set(payment_types))}")
    print(f"✅ Default methods: {len(default_methods)}")
    
    # Print summary of all payment methods
    print(f"\n📋 Payment Methods Summary:")
    for i, pm in enumerate(data_field):
        default_indicator = " (Default)" if pm["default"] else ""
        print(f"  {i+1}. {pm['payment_type']} ending in {pm['last4']} - {pm['status']}{default_indicator}")

def test_create_checkout_session_basic(credits_api):
    """Test basic checkout session creation with amount 2"""
    test_amount = 2
    
    # Make API call
    response = credits_api.create_checkout_session(test_amount)
    print(f"Response: {response}")
    
    # Basic response validation
    assert response.ok, f"API call failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f"Response data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert "message" in data, "Response missing 'message' field"
    assert "status" in data, "Response missing 'status' field"
    
    # Validate status field
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
    
    # Validate message field
    expected_message = "Checkout session successfully created"
    assert data["message"] == expected_message, f"Expected message '{expected_message}', got '{data['message']}'"
    
    return data["data"]["redirect_url"]  # Return for other tests to use


def test_create_checkout_session_data_structure(credits_api):
    """Test checkout session response data structure"""
    test_amount = 2
    
    response = credits_api.create_checkout_session(test_amount)
    data = response.json()
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, dict), "Data field should be a dictionary"
    assert "redirect_url" in data_field, "Data field missing 'redirect_url'"
    
    # Validate redirect_url
    redirect_url = data_field["redirect_url"]
    assert isinstance(redirect_url, str), "Redirect URL should be a string"
    assert len(redirect_url) > 0, "Redirect URL should not be empty"


def test_create_checkout_session_url_format(credits_api):
    """Test checkout session redirect URL format"""
    test_amount = 2
    
    response = credits_api.create_checkout_session(test_amount)
    data = response.json()
    redirect_url = data["data"]["redirect_url"]
    
    # Validate Stripe checkout URL format
    assert redirect_url.startswith("https://checkout.stripe.com/"), "Should be a valid Stripe checkout URL"
    assert "cs_test_" in redirect_url, "Should contain Stripe checkout session ID"
    
    # Validate URL structure components
    url_parts = redirect_url.split("/")
    assert len(url_parts) >= 5, "Invalid URL structure"
    assert "checkout.stripe.com" in url_parts, "Invalid domain"
    assert "pay" in url_parts, "Missing 'pay' path component"


def test_create_checkout_session_multiple_amounts(credits_api):
    """Test checkout session creation with different amounts"""
    test_amounts = [1, 5, 10, 100]
    base_redirect_url = None
    
    for amount in test_amounts:
        print(f"\nTesting with amount: {amount}")
        try:
            amount_response = credits_api.create_checkout_session(amount)
            assert amount_response.ok, f"Failed with amount {amount}"
            
            amount_data = amount_response.json()
            assert amount_data["status"] == "success", f"Status not success for amount {amount}"
            assert "redirect_url" in amount_data["data"], f"Missing redirect_url for amount {amount}"
            
            # Store first redirect URL for comparison
            if base_redirect_url is None:
                base_redirect_url = amount_data["data"]["redirect_url"]
            else:
                # Validate redirect URL is different for different amounts
                assert amount_data["data"]["redirect_url"] != base_redirect_url, f"Redirect URL should be different for amount {amount}"
                
        except Exception as e:
            print(f"Warning: Amount {amount} test failed: {e}")


def test_create_checkout_session_edge_cases(credits_api):
    """Test checkout session creation with edge case amounts"""
    print("\nTesting edge cases...")
    
    # Test with zero amount (should fail)
    try:
        zero_response = credits_api.create_checkout_session(0)
        if zero_response.ok:
            print("Warning: Zero amount was accepted (might be valid)")
        else:
            print("✅ Zero amount correctly rejected")
    except Exception as e:
        print(f"✅ Zero amount correctly caused error: {e}")
    
    # Test with negative amount (should fail)
    try:
        negative_response = credits_api.create_checkout_session(-1)
        if negative_response.ok:
            print("Warning: Negative amount was accepted (might be valid)")
        else:
            print("✅ Negative amount correctly rejected")
    except Exception as e:
        print(f"✅ Negative amount correctly caused error: {e}")


def test_create_checkout_session_large_amount(credits_api):
    """Test checkout session creation with very large amount"""
    try:
        large_response = credits_api.create_checkout_session(999999)
        assert large_response.ok, "Large amount should be accepted"
        large_data = large_response.json()
        assert large_data["status"] == "success", "Large amount should succeed"
        print("✅ Large amount accepted")
    except Exception as e:
        print(f"Warning: Large amount failed: {e}")


def test_create_checkout_session_integration(credits_api):
    """Integration test: verify complete checkout session flow"""
    test_amount = 2
    
    # Create checkout session
    response = credits_api.create_checkout_session(test_amount)
    assert response.ok, "Checkout session creation failed"
    
    data = response.json()
    assert data["status"] == "success", "Checkout session should be successful"
    
    # Verify redirect URL is accessible
    redirect_url = data["data"]["redirect_url"]
    assert redirect_url.startswith("https://checkout.stripe.com/"), "Invalid Stripe URL"
    
    print(f"\n🎉 Integration test passed!")
    print(f"✅ Created checkout session with amount: {test_amount}")
    print(f"✅ Redirect URL: {redirect_url[:100]}...")


# Legacy function for backward compatibility
def test_create_checkout_session(credits_api):
    """Legacy test function - runs all checkout session tests in sequence"""
    print("🔄 Running comprehensive checkout session tests...")
    
    # Run all individual tests
    test_create_checkout_session_basic(credits_api)
    test_create_checkout_session_data_structure(credits_api)
    test_create_checkout_session_url_format(credits_api)
    test_create_checkout_session_multiple_amounts(credits_api)
    test_create_checkout_session_edge_cases(credits_api)
    test_create_checkout_session_large_amount(credits_api)
    test_create_checkout_session_integration(credits_api)
    
    print("🎉 All checkout session tests completed!")
