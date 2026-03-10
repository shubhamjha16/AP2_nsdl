# NSDL-AP2-Agent

This project is a dedicated Proof of Concept (POC) for integrating the **Agent Payments Protocol (AP2)** with **NSDL Depository Operations**.

## Project Objective
Demonstrate how AI agents can automate and cryptographically secure securities delivery instructions (DIS), corporate actions, and portfolio rebalancing using the AP2 protocol.

## Repository Structure
- `src/ap2/`: Core AP2 protocol types and utility functions (Ported from the main AP2 repo).
- `day5_nsdl_instruction.py`: (Planned) End-to-end simulation of a securities transfer.
- `pyproject.toml`: Project configuration and dependencies.

## Key Concepts
- **Instruction Mandates**: Digitally signed agentic requests for securities movement.
- **Cryptographic Handoff**: A verifiable chain of trust from Investor -> DP -> NSDL.

## Getting Started
1. Install dependencies:
   ```sh
   uv pip install -e .
   ```
2. Run the NSDL demonstration:
   ```sh
   python3 day5_nsdl_instruction.py
   ```
