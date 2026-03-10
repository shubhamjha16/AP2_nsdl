# AP2: Global Standards & International Scalability

The **Agent Payments Protocol (AP2)** is designed to be **International by Default**. While the current POC is tailored for NSDL (India), the underlying architecture is built on global web and financial standards.

## 1. Global Technical Standards
AP2 leverages protocols accepted worldwide:
*   **W3C Payment Request API**: The standard used by browsers (Chrome, Safari) for payments globally.
*   **JWT & RS256**: International standards for secure, verifiable identity and non-repudiation.
*   **ISO 20022**: The protocol is designed to align with the global messaging standard used by SWIFT and modern Central Bank Digital Currencies (CBDCs).

## 2. Cross-Border Securities (The "Global Depository")
The logic we built for NSDL applies directly to global depository systems:
*   **USA (DTCC)**: The same "Agentic Instruction" model can automate delivery instructions for US stocks.
*   **Europe (Euroclear/Clearstream)**: AP2 can bridge the fragmented European markets by allowing agents to handle cross-border settlement instructions cryptographically.
*   **Emerging Markets**: AP2 provides a "Leapfrog" technology for countries without advanced digital depository systems, allowing them to skip manual slips and go directly to Zero-Trust architecture.

## 3. Global Commerce (The "Agentic Mall")
Because AP2 is merchant-agnostic:
*   An Indian user's agent can negotiate with a merchant in London or Dubai.
*   The `CartMandate` and `PaymentMandate` handle currency conversion and international shipping details using the same cryptographic handoff.
*   It solves the "Trust Gap" in international commerce—the merchant knows the payment is authorized by a verified agent, and the shopper knows the price is locked.

## 4. Why This Matters for Investors
When you pitch this to Rishabh or the NSDL CISO:
- **India as the Launchpad**: Use India's advanced digital stack (UPI/NSDL) to prove the protocol.
- **Global Export**: Position the company not just as an "Indian Startup" but as the creator of a **Global Protocol for Agentic Finance**.

**Status**: The code we have written uses ISIN numbers, which are the *International* standard for identifying securities. This makes the logic portable to any exchange in the world.
