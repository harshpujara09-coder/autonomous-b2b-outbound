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


⚡ Key Engineering Highlights
RFC 2822 Reply Threading Engine: Reverse-engineered thread persistence across Google Workspace and Microsoft 365 by extracting server Message-ID values from IMAP and injecting explicit In-Reply-To and References headers on Step 2 follow-ups.

Secondary Domain Isolation: Operates fully isolated dispatch infrastructure (outbound-domain.com) with 301 redirects to protect root domain reputation (primarybrand.com).

Multi-Tier Account Waterfalling: Prevents spamming entire organizations at once by staggering outreach across decision-makers first, automatically suppressing secondary operators until the initial cadence completes.

Deliverability Safeguards: Features strict human-cadence throttling (15–20 sends/day), zero-link first touches to clear Proofpoint/Defender filters, and automated suppression list verification.

Human-in-the-Loop Review Desk: Lightweight local dashboard allowing operator inspection, live draft regeneration, and manual queue authorization before any SMTP transaction fires.


🛠️ Tech Stack
Language: Python 3.11+

AI Engine: Anthropic Claude Code CLI

Infrastructure: SMTP/IMAP protocol handlers, SQLite

Deliverability: Custom domain warmup pacing & SPF/DKIM/DMARC compliance monitoring

🚀 Local Setup
Clone the repository:

Bash
git clone git@github.com:harshpujara09-coder/autonomous-b2b-outbound.git
cd autonomous-b2b-outbound
Configure environment:

Bash
cp .env.example .env
# Add your SMTP credentials and Anthropic authorization
Launch the dashboard:

Bash
source .venv/bin/activate
sellbird dashboard
