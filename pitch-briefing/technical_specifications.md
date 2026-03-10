# AP2 Protocol: Formal Technical Specifications

This document defines the exact cryptographic and logical requirements of the Agent Payments Protocol (AP2) as implemented across the **Agentic Commerce** and **NSDL Depository** projects.

## 1. Cryptographic Foundation

| Component | Standard | Purpose |
| :--- | :--- | :--- |
| **Identity** | RSA-2048 (PKCS#8) | Unique DIDs for Users, Merchants, DPs, and Depository Gateways. |
| **Hashing** | SHA-256 | Canonical JSON hashing for mandate integrity. |
| **Authorization** | RS256 (JWT) | Immutable signatures over mandate contents and transaction data. |

## 2. Verification Procedure (Processor / Gateway Level)
Every AP2-compliant gateway (whether for Commerce or NSDL) follows a deterministic verification algorithm:

1.  **Identity Resolve**: Map the `iss` (Issuer) DID from the JWT to the registered Public Key.
2.  **Signature Check**: Decrypt the JWT using the Public Key (`RS256`). If invalid, reject immediately (**Security Alert**).
3.  **Integrity Check**: Re-compute the SHA-256 hash of the received `MandateContents`. Compare it against the `transaction_data` in the JWT payload. If they don't match, reject (**Tamper Detection**).
4.  **Chain of Trust**: Ensure the `CartMandate` hash in the `PaymentMandate` matches the original cart commitment from the merchant/DP.

## 3. Implementation Rigor
- **Deterministic Serialization**: All implementations use `json.dumps(obj, sort_keys=True)` to ensure hashing is identical across platforms.
- **Pydantic Validation**: All data is validated against formal schemas before processing, preventing injection attacks.
- **Non-Repudiation**: Once signed, the instruction is legally binding and cannot be denied by the signer due to the nature of RSA signatures.
