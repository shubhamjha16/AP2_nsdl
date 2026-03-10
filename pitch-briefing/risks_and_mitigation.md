# AP2 Integration: Risks & Strategic Mitigations

For a CISO-level pitch, it is critical to address the drawbacks honestly. Moving to a decentralized, agentic instruction model introduces specific challenges.

## 1. Key Management & Recovery (The "Locked Account" Risk)
*   **Drawback**: Unlike a password, if a user loses their private cryptographic key (stored in their agent/TEE), they lose the ability to sign instructions. 
*   **Mitigation**: Implement **Social Recovery** or **Hardware Security Modules (HSM)**. NSDL could act as a "Key Recovery Service" where a secondary key is held in escrow to re-link an account.

## 2. Regulatory & Legal Lag
*   **Drawback**: Current SEBI regulations might require a DP's manual oversight. "Agentic Instructions" may not yet be legally recognized as equivalent to a physical/e-DIS signature.
*   **Mitigation**: Pitch this as a **Regulatory Sandbox** initiative. AP2 provides *better* non-repudiation than current logs, making it easier to convince regulators of its superiority.

## 3. Local Device Compromise
*   **Drawback**: If a user's phone/computer is fully compromised at the OS level, a malicious actor could force the agent to sign a mandate.
*   **Mitigation**: **Trusted Execution Environments (TEE)**. The private key never leaves the secure enclave of the hardware, requiring biometric (FaceID/Fingerprint) for every high-value instruction.

## 4. Systemic Agent Logic Errors ("Flash Crashes")
*   **Drawback**: A bug in a widely used shopping or investment agent could lead to millions of incorrect instructions being fired simultaneously.
*   **Mitigation**: **Circuit Breakers**. NSDL/DP level limits on agentic transaction frequency and volume (e.g., "Agent cannot move more than 5% of portfolio per hour").

## 5. Ecosystem Resistance (Intermediary Pushback)
*   **Drawback**: Traditional DPs and Brokers will see this as a threat to their business model (disintermediation).
*   **Mitigation**: Position AP2 as a **Efficiency Tool** for DPs first. Let them use it to lower *their* operational costs before opening it for full DP replacement.

## 7. Adoption Friction
*   **Drawback**: Users are used to OTPs and Portals. Switching to "Agent Consent" requires a behavioral shift.
*   **Mitigation**: **Invisible Crypto**. Use seamless wallet-abstraction so users feel like they are just "Approving a notification," while the crypto handoff happens in the background.

---

# AP2 for Agentic Commerce: Consumer & Merchant Risks

For the general commerce pitch (Rishabh), the focus shifts from institutional security to consumer trust and automated safety.

## 1. Intent Misalignment (The "Wrong Purchase" Risk)
*   **Drawback**: AI agents might misinterpret a user's natural language request (e.g., buying the wrong size or non-refundable tickets).
*   **Mitigation**: **Human-in-the-Loop (HITL) Guards**. The `IntentMandate` requires a final "User Tap" for summary confirmation before the `PaymentMandate` can be cryptographically signed by the agent.

## 2. Privacy Leakage (The "Oversharing" Risk)
*   **Drawback**: Agents might share too much personal data (address, preferences, full cart) with merchants while searching for prices.
*   **Mitigation**: **Zero-Knowledge Proofs (ZKP)** and **Contact Selection**. The protocol only reveals necessary data to the merchant once the match is confirmed, using `ap2_contact_picker` to limit exposure.

## 3. Automated Overspending ("Runaway Agent" Risk)
*   **Drawback**: Fully autonomous agents could theoretically keep making purchases if a loop or bug occurs, draining a user's wallet.
*   **Mitigation**: **Spending Limits & TTL**. Users set hard "Daily Mandate Limits" (e.g., ₹5,000 max per day) at the wallet/key level, which the agent cannot bypass.

## 4. Merchant "Ghosting" or Fulfillment Fraud
*   **Drawback**: A merchant might sign a `CartMandate` but fail to deliver goods after receiving payment authorized by the agent.
*   *Pitch*: AP2 creates an **Immutable Dispute Trail**. Because every step is signed, the user has cryptographically unbreakable proof that the merchant committed to a price and SKU, making chargebacks/refunds much easier for card networks to process.
