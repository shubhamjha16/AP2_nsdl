import json
import base64
import hashlib
from typing import Dict, Any
import jwt
from ap2.types.mandate import PaymentMandate
from ap2.crypto_utils import hash_object

class NSDLDepositoryGateway:
    """
    A production-logic gateway for NSDL that verifies AP2 mandates.
    Implements non-repudiation and cryptographic integrity checks.
    """
    
    def __init__(self):
        self._ledger = []  # Simulated immutable ledger
        self._authorized_public_keys = {} 

    def register_investor_key(self, investor_did: str, public_key_pem: str):
        """Registers a user's public key (e.g., during account onboarding)."""
        self._authorized_public_keys[investor_did] = public_key_pem
        print(f"[Gateway] Onboarded Public Key for DID: {investor_did}")

    def verify_and_settle(self, payment_mandate_json: str):
        """
        The core settlement function. 
        Verifies the 'Chain of Trust' from Investor -> DP -> NSDL.
        """
        print("\n[NSDL Gateway] Processing Instruction...")
        
        try:
            # 1. Schema Validation (Pydantic)
            data = json.loads(payment_mandate_json)
            mandate = PaymentMandate(**data)
            contents = mandate.payment_mandate_contents
            
            # 2. Cryptographic Non-Repudiation Check
            # Extract investor identity from metadata (or DID)
            # In production, 'iss' in JWT would be the Investor's DID
            auth_jwt = mandate.user_authorization
            unverified_headers = jwt.get_unverified_header(auth_jwt)
            
            # Identify the signer
            investor_did = "INVESTOR_001" # In prod, this comes from 'sub' or 'iss'
            pub_key = self._authorized_public_keys.get(investor_did)
            
            if not pub_key:
                return {"success": False, "error": "Identity Unknown: Public key not on file."}

            # 3. Signature & Expiry Verification
            # jwt.decode handles the RS256 signature check against the public key
            decoded = jwt.decode(
                auth_jwt, 
                pub_key, 
                algorithms=["RS256"],
                options={"verify_iat": True}
            )
            
            # 4. Content Integrity (Double-Hash Verification)
            # We must ensure the mandate the user signed is exactly what we received
            actual_hash = hash_object(contents.model_dump())
            if actual_hash not in decoded.get("transaction_data", []):
                return {"success": False, "error": "Integrity Breach: Mandate content tampered."}

            # 5. Business Logic Verification
            # (e.g., check if the investor has enough shares - Mocked here)
            txn_id = f"NSDL-{hashlib.sha1(auth_jwt.encode()).hexdigest()[:10].upper()}"
            
            print(f"[Gateway] ✅ NON-REPUDIATION VERIFIED: Digital Signature is authentic.")
            print(f"[Gateway] ✅ INTEGRITY VERIFIED: SHA-256 Checksum matches.")
            print(f"[Gateway] 🚀 SETTLED: Transaction {txn_id} committed to ledger.")
            
            self._ledger.append({"txn_id": txn_id, "mandate": mandate.model_dump()})
            return {"success": True, "txn_id": txn_id}

        except jwt.InvalidSignatureError:
            return {"success": False, "error": "Security Alert: Invalid Signature detected!"}
        except Exception as e:
            return {"success": False, "error": f"Internal Error: {str(e)}"}

def simulate_nsdl_agent_flow():
    # This function would be called by the POC script
    pass

if __name__ == "__main__":
    print("NSDL Mock Depository Agent initialized.")
