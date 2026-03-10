# Walkthrough: NSDL Depository Operations POC

This walkthrough demonstrates the end-to-end flow of a cryptographically signed securities delivery instruction (DIS) using the **Agent Payments Protocol (AP2)**.

## 1. Scenario Overview
An investor wants to transfer **100 shares of Reliance Industries Ltd (ISIN: INE002A01018)** to a specific account. Instead of a manual slip, they use their AP2-enabled agent.

## 2. Technical Components
- **Investor Agent**: Holds the investor's private key and generates the `SecuritiesIntentMandate`.
- **Depository Participant (DP) Agent**: Acting as the "Merchant," it verifies the intent and issues a signed `CartMandate` for the instruction.
- **AP2 Protocol**: The cryptographic glue ensuring that NSDL only settles instructions signed by the verified investor.

## 3. Step-by-Step Execution

### Step 1: Generating Instruction Intent
The investor defines the transfer details.
```python
sec_details = SecuritiesMandate(
    isin="INE002A01018", 
    quantity=100,
    instruction_type="TRANSFER",
    ...
)
```

### Step 2: DP Signature (Cart Mandate)
The DP signs the instruction details, guaranteeing that if the user authorizes it, the DP will settle it at NSDL.
> **Verification Output**: `DP Auth Signature (JWT): eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMjQwOTA...`

### Step 3: Investor Final Authorization (Payment Mandate)
The investor signs over the instruction and the DP's confirmation.
> **Verification Output**: `Investor Auth Signature (JWT): eyJhbGciOiJFUzI1NksiLCJraWQiOiJkaWQ6ZXhhbXBsZ...`

### Step 4: NSDL Final Verification (Hardened Gateway)
The NSDL server (now `NSDLDepositoryGateway`) verifies the cryptographic signature of the investor and the integrity of the mandate.
> **Final Output**: `[Gateway] ✅ NON-REPUDIATION VERIFIED | ✅ INTEGRITY VERIFIED`

## 5. Engineering Rigor & Tests
To move beyond "vibe coding," we have implemented:
- **Formal Specs**: Defined in [technical_specifications.md](file:///Users/apple/.gemini/antigravity/brain/574f01ce-d0da-4489-acd9-4757beb34e22/technical_specifications.md).
- **Unit Tests**: Run `python3 protocol_test.py` to see the protocol reject tampered instructions in real-time.

## 6. Run the Simulation
Navigate to the `NSDL-AP2-Agent` project and run:
```sh
python3 day5_nsdl_instruction.py
```
