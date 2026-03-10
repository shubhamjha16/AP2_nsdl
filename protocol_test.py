import json
import unittest
from ap2.crypto_utils import generate_key_pair, get_private_key_pem, get_public_key_pem, sign_cart_mandate, sign_payment_mandate, hash_object
from nsdl_depository_agent import NSDLDepositoryGateway
from ap2.types.mandate import PaymentMandate, PaymentMandateContents
from ap2.types.payment_request import PaymentItem, PaymentCurrencyAmount, PaymentResponse

class TestAP2NSDLProtocol(unittest.TestCase):
    def setUp(self):
        self.gateway = NSDLDepositoryGateway()
        self.investor_priv, self.investor_pub = generate_key_pair()
        self.investor_priv_pem = get_private_key_pem(self.investor_priv)
        self.investor_pub_pem = get_public_key_pem(self.investor_pub)
        self.gateway.register_investor_key("INVESTOR_001", self.investor_pub_pem)

    def test_valid_settlement(self):
        """Test a perfectly signed and matched instruction."""
        payment_contents = PaymentMandateContents(
            payment_mandate_id="pm_test_001",
            payment_details_id="txn_test",
            payment_details_total=PaymentItem(label="Total", amount=PaymentCurrencyAmount(currency="INR", value=10.0)),
            payment_response=PaymentResponse(request_id="txn_test", method_name="MOCK", details={}),
            merchant_agent="Test DP"
        )
        mandate = PaymentMandate(payment_mandate_contents=payment_contents)
        
        # Sign the mandate
        mock_cart_hash = "fake_cart_hash_123"
        mandate.user_authorization = sign_payment_mandate(
            payment_contents.model_dump(),
            mock_cart_hash,
            self.investor_priv_pem
        )
        
        result = self.gateway.verify_and_settle(json.dumps(mandate.model_dump()))
        self.assertTrue(result["success"])
        self.assertIn("NSDL-", result["txn_id"])

    def test_tamper_detection(self):
        """Test that modifying the mandate after signing causes a failure."""
        payment_contents = PaymentMandateContents(
            payment_mandate_id="pm_test_001",
            payment_details_id="txn_test",
            payment_details_total=PaymentItem(label="Total", amount=PaymentCurrencyAmount(currency="INR", value=10.0)),
            payment_response=PaymentResponse(request_id="txn_test", method_name="MOCK", details={}),
            merchant_agent="Test DP"
        )
        mandate = PaymentMandate(payment_mandate_contents=payment_contents)
        
        # Sign the ORIGINAL mandate
        mock_cart_hash = "fake_cart_hash_123"
        mandate.user_authorization = sign_payment_mandate(
            payment_contents.model_dump(),
            mock_cart_hash,
            self.investor_priv_pem
        )
        
        # TAMPER: Change the amount after signing
        mandate.payment_mandate_contents.payment_details_total.amount.value = 999999.0
        
        result = self.gateway.verify_and_settle(json.dumps(mandate.model_dump()))
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Integrity Breach: Mandate content tampered.")

if __name__ == '__main__':
    unittest.main()
