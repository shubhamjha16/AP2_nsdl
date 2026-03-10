# What does a DP actually do? (And how Agents replace them)

A Depository Participant (DP) acts as the bridge between the Investor and NSDL. Here is exactly what they do today, and how the **AP2 Agent** changes the game.

## Core DP Functions vs. AP2 Agents

| DP Function | Traditional Process (Human-Mediated) | AP2 Agent Process (Autonomous/Signed) |
| :--- | :--- | :--- |
| **Instruction Processing (DIS)** | You sign a physical slip or login to a portal to "tell" the DP to move shares. | **Signed Mandate**: The agent generates and signs a cryptographically verifiable instruction (DIS replacement) instantly. |
| **Pledge & Hypothecation** | Manual request to "lock" shares for a loan; DP coordinates with lender. | **Automated Pledge**: Agent "locks" shares as collateral in response to a loan mandate. |
| **Account Maintenance** | Charging annual maintenance fees (AMC), updating addresses, KYC. | **Self-Sovereign Identity**: Agent carries verified claims (VCs) and updates the registry via protocol messages. |
| **Transaction Recording** | Every trade is logged in the DP's proprietary ledger before syncing with NSDL. | **Real-Time Sync**: Every mandate is a direct, verifiable instruction to the NSDL "Golden Record". |
| **Corporate Actions** | DP receives dividend/bonus and credits it to your account (delayed). | **Instant Routing**: Agent receives "Cart Mandate" (Dividend) and routes it to the correct portfolio immediately. |
| **Security & Verification** | DP verifies your signature or 2FA (often weak). | **RSA/JWT Cryptography**: Zero-trust verification. No human at the DP can "override" or "fake" your agent's signature. |

## The "Invisible" DP
In the AP2 model, the **DP becomes a Pure API**. 
- **Today**: You "use" a DP (Zerodha, HDFC, ICICI).
- **Tomorrow**: You "use" an Agent (PortfolioAI, TaxAgent), and they simply "plug into" a white-label DP utility that exists only to fulfill the legal custody requirement.

## Why this is a "Replacement"
When the Agent handles the **Intent**, the **Instruction**, and the **Security**, the DP is no longer "doing" the work. They are just a licensed entity waiting for the Agent's mandates. The high fees (AMC, Transaction charges) currently paid for "service" will collapse because the Agent does the service for free.
