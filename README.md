# Autonomous B2B Outbound Engine & Intelligence Pipeline

An event-driven, account-based outbound acquisition engine engineered in Python with Claude Code. Designed to replace $300+/mo outbound software stacks (Clay, Apollo, Smartlead) with a lightweight, domain-isolated ~$12/mo architecture tailored for targeting mid-to-enterprise engineering and consulting firms.

---

## 🏗️ System Architecture & Workflow

```text
[ SERP & Domain Discovery ]
             │
             ▼
[ Verification & Lead Scoring (Reoon / MX Validation) ]
             │
             ▼
[ Multi-Tier Account Waterfall ] ──► (Holds secondary contacts in reserve)
             │
             ▼
[ Claude Code Contextual Personalization ]
             │
             ▼
[ Human-in-the-Loop Review Desk (Local UI) ]
             │
             ▼
[ RFC 2822 SMTP Dispatcher ] ──► Injects In-Reply-To & References for Native Threading
