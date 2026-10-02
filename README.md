# AgenticAI

> IBM watsonx Orchestrate agents, tools, and knowledge bases — built and managed with the [watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com).

---

## Repository Overview

This repository contains ready-to-deploy IBM watsonx Orchestrate assets including native agents, Python tools, knowledge bases, and supporting scripts. All resources follow the `AG_SIM` naming prefix convention and are organised for dependency-ordered import.

---

## Project Structure

```
AgenticAI/
├── agents/                     # Agent YAML definitions
│   └── AG_hr_onboarding_agent.yaml
├── tools/                      # Python @tool files
│   └── AG_SIM_onboarding_tools.py
├── knowledge-bases/             # Knowledge base YAML specs + source documents
│   ├── AG_SIM_hr_knowledge_base.yaml
│   └── AG_SIM_hr_policies/
│       ├── company_handbook.txt
│       ├── employee_benefits.txt
│       └── onboarding_procedures.txt
├── connections/                 # Connection YAML definitions
├── models/                      # Custom model definitions
├── toolkits/                    # MCP toolkit configurations
├── scripts/
│   ├── import-all.sh            # Dependency-ordered import script
│   └── delete-all.sh            # Cleanup script (reverse order)
├── tests/
│   ├── TEST_REPORT.md           # Smoke test results
│   └── AG_hr_onboarding_agent_test_questions.docx
└── .bob/
    └── mcp.json                 # Bob MCP server configuration
```

---

## Agents

### `AG_hr_onboarding_agent`

A native IBM watsonx Orchestrate agent that guides new Acme Corporation employees through their complete onboarding journey.

**Capabilities:**
- Welcomes new employees by name and explains the 90-day onboarding process
- Answers questions about company policies, employee benefits, and standard procedures using a grounded knowledge base
- Guides employees step-by-step through all required paperwork (tax forms, NDA, equipment request, and more)
- Routes employees to the correct HR team or contact for questions outside its knowledge
- Generates a personalised onboarding checklist at the end of each session
- Maintains a friendly, patient, and encouraging tone throughout

| Property | Value |
|---|---|
| Kind | `native` |
| Style | `react_core` |
| LLM | `groq/openai/gpt-oss-120b` |
| Knowledge Base | `AG_SIM_hr_knowledge_base` |
| Tools | `AG_SIM_get_required_paperwork`, `AG_SIM_get_hr_contacts`, `AG_SIM_generate_onboarding_checklist` |

---

## Tools

All tools are prefixed `AG_SIM_` and live in [`tools/AG_SIM_onboarding_tools.py`](tools/AG_SIM_onboarding_tools.py).

| Tool | Permission | Description |
|---|---|---|
| `AG_SIM_get_required_paperwork` | `READ_ONLY` | Returns all 8 onboarding forms with descriptions, submission methods, deadlines, and contacts |
| `AG_SIM_get_hr_contacts` | `READ_ONLY` | Returns the full HR contact directory (9 teams) for routing out-of-scope questions |
| `AG_SIM_generate_onboarding_checklist` | `READ_ONLY` | Generates a personalised 14-item onboarding checklist for a given employee name |

---

## Knowledge Base

**`AG_SIM_hr_knowledge_base`** — built-in Milvus (managed, no external infrastructure required).

| Document | Contents |
|---|---|
| `company_handbook.txt` | Code of conduct, working hours, leave policy, expense policy, IT security, disciplinary procedure |
| `employee_benefits.txt` | Health insurance plans, 401(k), life & disability insurance, EAP, L&D, wellness perks |
| `onboarding_procedures.txt` | Paperwork checklist, system access, Day 1 orientation schedule, key contacts, 90-day milestones |

---

## Prerequisites

- Python ≥ 3.11, < 3.15
- `ibm-watsonx-orchestrate` ADK installed (`pip install ibm-watsonx-orchestrate`)
- An active watsonx Orchestrate environment (SaaS or local Developer Edition)
- A configured and activated `orchestrate` environment (`orchestrate env activate <name>`)

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/agdel1921/AgenticAI.git
cd AgenticAI
```

### 2. Set up the virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install ibm-watsonx-orchestrate
```

### 3. Activate your watsonx Orchestrate environment

```bash
orchestrate env activate <your-env-name>
orchestrate agents list   # confirm connection
```

### 4. Import all resources

```bash
chmod +x scripts/import-all.sh
./scripts/import-all.sh
```

This imports resources in dependency order:
1. Knowledge base (`AG_SIM_hr_knowledge_base`)
2. Tools (`AG_SIM_onboarding_tools.py`)
3. Agent (`AG_hr_onboarding_agent`)

### 5. Check knowledge base indexing

```bash
orchestrate knowledge-bases status -n AG_SIM_hr_knowledge_base
```

Wait until `Ready: True` before testing.

### 6. Test the agent

**Via Bob:**
```
Chat with AG_hr_onboarding_agent: Hi! My name is Alex and today is my first day. What does onboarding involve?
```

**Via CLI:**
```bash
orchestrate chat ask -n AG_hr_onboarding_agent "Hi! My name is Alex and today is my first day." -r
```
> ⚠️ The `-r` flag shows the reasoning trace. On SaaS this command may hang — prefer the Bob method above.

**Via wxO UI:**  
Open `AG_hr_onboarding_agent` in the watsonx Orchestrate web UI and use the starter prompts or type directly.

---

## Sample Test Questions

See [`tests/AG_hr_onboarding_agent_test_questions.docx`](tests/AG_hr_onboarding_agent_test_questions.docx) for the full set of 40 test questions across 7 categories, or use these quick starters:

| # | Question | What to verify |
|---|---|---|
| 1 | `Hi, my name is Jordan. It's my first day — what does onboarding involve?` | Greeted by name; 90-day plan explained |
| 2 | `What forms do I need to complete this week?` | `AG_SIM_get_required_paperwork` fires; NDA/I-9 highlighted as Day 1 |
| 3 | `What health insurance options do I have?` | KB queried; Platinum PPO, Gold HMO, Silver HDHP described accurately |
| 4 | `Who do I contact about my pay?` | `AG_SIM_get_hr_contacts` fires; Payroll team routed |
| 5 | `I'm done for today — can you give me a checklist? My name is Sam.` | `AG_SIM_generate_onboarding_checklist("Sam")` fires; 14-item list returned |

---

## Cleanup

To remove all deployed resources:

```bash
chmod +x scripts/delete-all.sh
./scripts/delete-all.sh
```

---

## Naming Conventions

| Prefix | Applies to |
|---|---|
| `AG_SIM_` | All tools, knowledge bases, and connections |
| `AG_` | Agent names |

---

## Test Report

Latest test results: [`tests/TEST_REPORT.md`](tests/TEST_REPORT.md)

**Status: Deployed and tested (2/2)**  
Both single-turn and multi-turn smoke tests passed. Tools fired correctly, knowledge base returned grounded answers, and multi-turn context (employee name) was retained across turns.

---

## License

This repository contains simulated demonstration assets for IBM watsonx Orchestrate. All company names, policies, and data within the knowledge base documents are fictional and intended for testing purposes only.

---

## Author

**ANGREJ**
