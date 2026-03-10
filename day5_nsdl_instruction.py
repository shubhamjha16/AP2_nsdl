import json
from ap2.types.mandate import CartContents, CartMandate, SecuritiesIntentMandate, SecuritiesMandate, PaymentMandate, PaymentMandateContents
from ap2.types.payment_request import PaymentRequest, PaymentDetailsInit, PaymentItem, PaymentCurrencyAmount, PaymentMethodData, PaymentResponse
from ap2.crypto_utils import generate_key_pair, get_private_key_pem, get_public_key_pem, sign_cart_mandate, sign_payment_mandate, hash_object
from datetime import datetime, timedelta, timezone

from nsdl_depository_agent import NSDLDepositoryGateway

def run_nsdl_instruction_demo():
    print("--- Day 5: NSDL Depository Operations (Securities Transfer) ---")

    # 1. Setup Keys for Investor and Depository Participant (DP)
    print("\n[Step 1] Generating Investor and DP RSA Key Pairs...")
    dp_priv, dp_pub = generate_key_pair()
    investor_priv, investor_pub = generate_key_pair()

    dp_priv_pem = get_private_key_pem(dp_priv)
    dp_pub_pem = get_public_key_pem(dp_pub)
    investor_priv_pem = get_private_key_pem(investor_priv)
    investor_pub_pem = get_public_key_pem(investor_pub)

    # Initialize NSDL Gateway
    gateway = NSDLDepositoryGateway()
    gateway.register_investor_key("INVESTOR_001", investor_pub_pem)

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

    # 3. DP (Acting as Merchant) creates and signs a CartMandate
    print("\n[Step 3] DP Generating Signed Instruction Confirmation (CartMandate)...")
    
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

    print(f"DP Auth Signature (JWT) generated.")

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

    print(f"Investor Auth Signature (JWT) generated.")

    # 5. NSDL Final Verification & Settlement
    print("\n[Step 5] DP Submitting Instruction to NSDL for Final Settlement...")
    result = gateway.verify_and_settle(json.dumps(payment_mandate.model_dump()))
    
    if result["success"]:
        print("\n[SUCCESS] NSDL Transaction Settled. TXN ID:", result["txn_id"])
        print("Protocol Integrity Proof: RSA Signature Verified | SHA-256 Hashes Matched.")
    else:
        print("\n[FAIL] Settlement Rejected:", result["error"])

    print("-" * 50)

if __name__ == "__main__":
    run_nsdl_instruction_demo()
