# TEST REPORT — AG_hr_onboarding_agent

**Status:** Deployed and tested (2/2)
**Date:** 2025
**Environment:** draft

---

## Test Results

| Turn | Prompt | Tools Used | Result | Pass |
|------|--------|-----------|--------|------|
| 1 | "Hi! My name is Jordan Smith and today is my very first day at Acme. Can you welcome me and tell me what the onboarding process involves?" | None (instructions only) | Warm welcome by name, clear 90-day journey table, offered help with paperwork/benefits/checklist | ✅ Pass |
| 2 (same thread) | "Thanks! Can you walk me through all the paperwork I need to complete? Also what are my health insurance options?" | `AG_SIM_get_required_paperwork` + `AG_SIM_hr_knowledge_base` | Retained Jordan's name from Turn 1; returned all 8 forms in priority order; returned accurate health insurance options from KB | ✅ Pass |

**Pass criteria met:**
- No errors ✅
- Correct, grounded output (KB-sourced) ✅
- Correct tools fired (verified from reasoning trace) ✅
- Turn 2 used context (name) from Turn 1 ✅

---

## How to Test Manually

### UI
Open `AG_hr_onboarding_agent` in the watsonx Orchestrate web UI and use the starter prompts or type directly.

### CLI
```bash
source venv/bin/activate
orchestrate chat ask -n AG_hr_onboarding_agent "<prompt>" -r
```
> ⚠️ On SaaS this can hang — prefer the Bob chat command below.

### Bob
*"Chat with `AG_hr_onboarding_agent`: `<prompt>`"*

---

## Sample Prompts (with expected outcomes)

| # | Prompt | Expected Output |
|---|--------|-----------------|
| 1 | `Hi! My name is Alex and today is my first day. What does onboarding involve?` | Warm welcome using "Alex", 90-day overview table, offer to help with paperwork/benefits/checklist |
| 2 | `What forms do I need to complete in my first week?` | `AG_SIM_get_required_paperwork` fires; 8 forms returned in deadline order, NDA/I-9 highlighted as Day 1 |
| 3 | `Can you tell me about the 401(k) and retirement benefits?` | KB queried; returns Fidelity 401(k) detail: 6% match, 4-yr vesting, auto-enrol at 3%, Roth option |
| 4 | `Who do I contact for questions about my health insurance?` | `AG_SIM_get_hr_contacts` fires; benefits@acme.com + +1(415)555-0200 returned |
| 5 | `I'm done for the day. Can you give me my onboarding checklist? My name is Sam.` | `AG_SIM_generate_onboarding_checklist("Sam")` fires; 14-item checklist returned; encouraging close |
