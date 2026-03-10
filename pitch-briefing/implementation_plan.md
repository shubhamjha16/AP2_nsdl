# Implementation Plan: NSDL Depository Operations POC

This plan outlines the steps to create a technical demonstration of how AP2's cryptographic handoff can be used for securities delivery instructions (DIS) at NSDL.

## Proposed Changes

### AP2 Core Enhancements

#### [MODIFY] [mandate.py](file:///Users/apple/Desktop/agenticcommercev1/NSDL-AP2-Agent/src/ap2/types/mandate.py)
- Add `SecuritiesMandate` or extend `IntentMandate` to include securities-specific fields like `isin`, `quantity`, and `target_dp_id`.

### New Demonstration

#### [NEW] [day5_nsdl_instruction.py](file:///Users/apple/Desktop/agenticcommercev1/NSDL-AP2-Agent/day5_nsdl_instruction.py)
- A new script that simulates:
    1. An Investor Agent creating a `SecuritiesIntentMandate`.
    2. A Depository Participant (DP) Agent acting as the "Merchant" to verify and sign a `CartMandate` for the transfer.
    3. The Investor signing the `PaymentMandate` (Authorization) to settle the instruction.

## Verification Plan

### Automated Tests
- Run `python3 day5_nsdl_instruction.py` and verify the cryptographic signatures are valid across the chain (Investor -> DP -> NSDL).

### Manual Verification
- Review the generated Mandate JSONs in the console output to ensure they comply with NSDL's reporting requirements (e.g., proper ISIN format).
