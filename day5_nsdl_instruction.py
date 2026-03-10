import json
from ap2.types.mandate import CartContents, CartMandate, SecuritiesIntentMandate, SecuritiesMandate, PaymentMandate, PaymentMandateContents
from ap2.types.payment_request import PaymentRequest, PaymentDetailsInit, PaymentItem, PaymentCurrencyAmount, PaymentMethodData
from ap2.types.payment_response import PaymentResponse
from ap2.crypto_utils import generate_key_pair, get_private_key_pem, sign_cart_mandate, sign_payment_mandate, hash_object
from datetime import datetime, timedelta, timezone

def run_nsdl_instruction_demo():
    print("--- Day 5: NSDL Depository Operations (Securities Transfer) ---")

    # 1. Setup Keys for Investor and Depository Participant (DP)
    print("\n[Step 1] Generating Investor and DP RSA Key Pairs...")
    dp_priv, dp_pub = generate_key_pair()
    investor_priv, investor_pub = generate_key_pair()

    dp_priv_pem = get_private_key_pem(dp_priv)
    investor_priv_pem = get_private_key_pem(investor_priv)

    # 2. Create a Securities Intent Mandate (The "Digital DIS")
    print("\n[Step 2] Investor Creating Securities Intent Mandate (Digital DIS)...")
    sec_details = SecuritiesMandate(
        isin="INE002A01018",  # Reliance Industries Ltd.
        quantity=100,
        instruction_type="TRANSFER",
        target_dp_id="DP12345",
        target_client_id="ACC67890",
        execution_date=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        reason_code="01" # Gift/Off-market transfer
    )
    
    intent = SecuritiesIntentMandate(
        natural_language_description="Transfer 100 shares of Reliance to my son's account.",
        intent_expiry=(datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
        securities_details=sec_details
    )
    print(f"Intent: {intent.natural_language_description}")
    print(f"ISIN: {intent.securities_details.isin} | Quantity: {intent.securities_details.quantity}")

    # 3. DP (Acting as Merchant) creates and signs a CartMandate
    print("\n[Step 3] DP Generating Signed Instruction Confirmation (CartMandate)...")
    
    # In securities, the "PaymentRequest" can include stamp duty and transaction charges
    payment_request = PaymentRequest(
        method_data=[PaymentMethodData(supported_methods="DP_WALLET")],
        details=PaymentDetailsInit(
            id="txn_nsdl_987",
            display_items=[
                PaymentItem(label="Stamp Duty", amount=PaymentCurrencyAmount(currency="INR", value=15.00)),
                PaymentItem(label="DP Charges", amount=PaymentCurrencyAmount(currency="INR", value=50.00))
            ],
            total=PaymentItem(label="Total Charges", amount=PaymentCurrencyAmount(currency="INR", value=65.00))
        )
    )

    contents = CartContents(
        id="cart_nsdl_555",
        user_cart_confirmation_required=True,
        payment_request=payment_request,
        cart_expiry=(datetime.now(timezone.utc) + timedelta(minutes=60)).isoformat(),
        merchant_name="SafeCustody DP Services"
    )

    cart_mandate = CartMandate(contents=contents)
    cart_mandate.merchant_authorization = sign_cart_mandate(contents.model_dump(), dp_priv_pem)

    print(f"DP Auth Signature (JWT): {cart_mandate.merchant_authorization[:50]}...")

    # 4. Investor Authorizes with a PaymentMandate (Final Authorization)
    print("\n[Step 4] Investor Signing Final Authorization (PaymentMandate)...")

    payment_response = PaymentResponse(
        request_id=payment_request.details.id,
        method_name="DP_WALLET",
        details={"auth_token": "dp_secure_token_abc"}
    )

    payment_contents = PaymentMandateContents(
        payment_mandate_id="pm_nsdl_111",
        payment_details_id=payment_request.details.id,
        payment_details_total=payment_request.details.total,
        payment_response=payment_response,
        merchant_agent="SafeCustody DP Services"
    )

    payment_mandate = PaymentMandate(payment_mandate_contents=payment_contents)

    # Chain of Trust: Sign over both the DP's Cart Mandate and the Payment Details
    cart_hash = hash_object(cart_mandate.model_dump())
    payment_mandate.user_authorization = sign_payment_mandate(
        payment_contents.model_dump(),
        cart_hash,
        investor_priv_pem
    )

    print(f"Investor Auth Signature (JWT): {payment_mandate.user_authorization[:50]}...")

    print("\n[Success] NSDL Instruction Verified!")
    print("Verifiable chain established: Investor -> DP -> NSDL Settlement.")
    print("-" * 50)
    print("Summary of Mandate JSON:")
    print(json.dumps(payment_mandate.model_dump(), indent=2)[:500] + "...")

if __name__ == "__main__":
    run_nsdl_instruction_demo()
