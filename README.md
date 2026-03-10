# NSDL-AP2-Agent: Hardened Depository POC

This project is a dedicated, **Production-Logic Proof of Concept (POC)** for integrating the **Agent Payments Protocol (AP2)** with **NSDL Depository Operations**.

## Project Objective
Demonstrate how AI agents can automate and cryptographically secure securities delivery instructions (DIS), corporate actions, and portfolio rebalancing using the AP2 protocol.

## 🚀 Hardened Status: "Engineering Ready"
- **NSDL Depository Gateway**: Implemented a hardened gateway with RSA-2048 non-repudiation and SHA-256 integrity verification.
- **Tamper Detection**: Catch and reject modified instructions in real-time.
- **Formal Specs**: Defined in `pitch-briefing/technical_specifications.md`.

## Repository Structure
- `src/ap2/`: Core AP2 protocol types and utility functions.
- `day5_nsdl_instruction.py`: Hardened end-to-end simulation of a securities transfer.
- `protocol_test.py`: Unit tests proving technical rigor and tamper-detection.
- `pitch-briefing/`: Professional artifacts for the CISO pitch (Security Brief, Financials, Risks).

## Getting Started
1. Install dependencies:
   ```sh
   uv pip install -e .
   ```
2. Run the unit tests (Proof of Math):
   ```sh
   python3 protocol_test.py
   ```
3. Run the NSDL demonstration:
   ```sh
   python3 day5_nsdl_instruction.py
   ```
