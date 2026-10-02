"""Generate AG_hr_onboarding_agent_test_questions.docx using python-docx."""
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT = Path(__file__).parent / "AG_hr_onboarding_agent_test_questions.docx"

CATEGORIES = [
    {
        "title": "Category 1 — Welcome & Onboarding Overview",
        "subtitle": "Tests: greeting by name, explaining the 90-day process, friendly tone.",
        "rows": [
            ("1.1", "Hi, my name is Priya Sharma and it's my first day. Can you welcome me and walk me through what onboarding looks like?",
             "Uses 'Priya' by name; covers 90-day journey table (Week 1 admin, Weeks 2-4 training, Day 30/60/90 milestones); warm, encouraging tone throughout."),
            ("1.2", "I'm starting tomorrow. What should I expect in my first week?",
             "Describes Day 1 schedule: lobby reception at 9am, HR induction, IT setup, buddy assignment, manager 1:1 at 3pm."),
            ("1.3", "What is the onboarding process at Acme?",
             "Returns 90-day programme overview; mentions paperwork checklist, system access, orientation, and probation period."),
        ],
    },
    {
        "title": "Category 2 — Paperwork (Step-by-Step Guidance)",
        "subtitle": "Tests: AG_SIM_get_required_paperwork tool call, correct deadlines, Day 1 prioritisation.",
        "rows": [
            ("2.1", "What forms do I need to fill in before my start date?",
             "AG_SIM_get_required_paperwork fires; NDA flagged as pre-start/Day 1 priority; DocuSign method mentioned."),
            ("2.2", "Can you explain what the NDA is and how I sign it?",
             "Describes NDA scope (trade secrets, client data); DocuSign link to personal email; legal@acme.com for questions."),
            ("2.3", "I forgot to bring my ID documents today. What happens with the I-9?",
             "States I-9 requires original documents in person at HR reception Level 2; contact hr@acme.com."),
            ("2.4", "How do I request my laptop and equipment?",
             "Equipment Request Form at it.acme.internal/equipment-request; submit by end of Day 1; IT provisions within 48 hours."),
            ("2.5", "What is the deadline for completing my tax forms?",
             "W-4 within 3 business days; state withholding form also mentioned; payroll portal for direct deposit setup."),
            ("2.6", "Walk me through the paperwork one step at a time — starting with the most urgent items.",
             "Agent leads with NDA, I-9, Equipment Request (all Day 1); then W-4, direct deposit, handbook acknowledgement (3 days)."),
        ],
    },
    {
        "title": "Category 3 — Company Policies",
        "subtitle": "Tests: KB retrieval from company_handbook.txt; accurate, grounded answers.",
        "rows": [
            ("3.1", "How many days of annual leave do I get?",
             "25 days per year, prorated for part-year starters, monthly accrual."),
            ("3.2", "Can I work from home? What is the remote work policy?",
             "Up to 3 remote days/week; on-site Tuesdays and Thursdays by default; manager approval for flex hours."),
            ("3.3", "What are the standard working hours?",
             "9:00 AM to 5:30 PM; core hours 10am to 3pm; 30-minute notification rule for absences or late arrival."),
            ("3.4", "What happens if I'm sick and need to take time off?",
             "10 paid sick days per year; no carry-over; notify manager 30 minutes before scheduled start."),
            ("3.5", "What is Acme's code of conduct? What behaviour is expected of me?",
             "Respect, professionalism, confidentiality, no conflicts of interest, no discrimination; violations lead to disciplinary action up to termination."),
            ("3.6", "I'm going on parental leave soon. How much leave do I get?",
             "26 weeks fully paid for primary caregiver; 4 weeks for secondary caregiver; submit via HR Portal."),
            ("3.7", "What is Acme's policy on expense claims?",
             "Pre-approval for expenses over $500; submit within 30 days; receipts required for expenses over $25; per diem $75 domestic / $120 international."),
        ],
    },
    {
        "title": "Category 4 — Employee Benefits",
        "subtitle": "Tests: KB retrieval from employee_benefits.txt; accurate, grounded answers.",
        "rows": [
            ("4.1", "What health insurance plans are available to me?",
             "Platinum PPO ($250 deductible, Acme covers 90%), Gold HMO ($500, 85%), Silver HDHP ($1,500 with $600 HSA seed)."),
            ("4.2", "Does Acme offer dental and vision coverage?",
             "Dental: 100%/80%/50% tiers, $2,500 annual max. Vision: $250 frames, $200 contacts, 100% annual eye exam."),
            ("4.3", "How does the 401(k) matching work?",
             "Dollar-for-dollar up to 6% of salary; 4-year vesting (25%/yr); auto-enrolled at 3%; Fidelity portal; Roth option available."),
            ("4.4", "Is there a gym or wellness benefit?",
             "$600/year gym reimbursement; subsidised Calm/Headspace; $300 ergonomic home-office allowance; quarterly wellness challenges."),
            ("4.5", "What learning and development support does Acme offer?",
             "$2,000/year L&D budget; LinkedIn Learning unlimited; tuition reimbursement up to $5,250/year; internal mentoring programme."),
            ("4.6", "I have a dependent. Are they covered under my health insurance?",
             "Confirms all full-time employees and eligible dependants are covered from Day 1."),
            ("4.7", "When do I need to enrol in benefits?",
             "Within 30 days of hire at benefits.acme.internal; changes only at Open Enrolment (November) or Qualifying Life Event."),
        ],
    },
    {
        "title": "Category 5 — Contact Routing",
        "subtitle": "Tests: AG_SIM_get_hr_contacts tool call; routing to the correct team for each query type.",
        "rows": [
            ("5.1", "I haven't received my DocuSign link for the NDA. Who do I contact?",
             "Routes to Legal team: legal@acme.com / Ext. 6000."),
            ("5.2", "My laptop hasn't arrived yet. Who can help?",
             "Routes to IT Helpdesk: helpdesk@acme.com / Ext. 4000."),
            ("5.3", "I want to dispute something about my pay. Who handles that?",
             "Routes to Payroll: payroll@acme.com / Ext. 5100."),
            ("5.4", "I'd like to report a concern confidentially. How do I do that?",
             "Routes to Ethics Hotline: ethics@acme.com / 1-800-555-0199; highlights the confidentiality guarantee."),
            ("5.5", "I have a question about my building access and parking.",
             "Routes to Facilities: facilities@acme.com / Ext. 3000."),
            ("5.6", "I want to raise a conflict that involves my manager. Who is the right person?",
             "Routes to HR Business Partner: hr-bp@acme.com; describes HRBP scope (escalated issues, team conflicts)."),
        ],
    },
    {
        "title": "Category 6 — Checklist & Session Summary",
        "subtitle": "Tests: AG_SIM_generate_onboarding_checklist tool call, end-of-session behaviour, and summary quality.",
        "rows": [
            ("6.1", "Can you give me my onboarding checklist? My name is Maria Chen.",
             "AG_SIM_generate_onboarding_checklist('Maria Chen') fires; 14-item checklist with Maria's name; urgent items highlighted; encouraging close."),
            ("6.2", "I think I'm done for today. Can you summarise what I need to do?",
             "Agent detects session end; generates personalised checklist; breaks down Day 1, 3-day, and 30-day tasks clearly."),
            ("6.3", "Give me a checklist of everything I still need to complete during onboarding.",
             "Full 14-item list with deadlines; no fabricated items outside the tool output."),
        ],
    },
    {
        "title": "Category 7 — Multi-turn & Edge Cases",
        "subtitle": "Tests: context retention across turns, out-of-scope deflection, graceful escalation, and patience under confusion.",
        "rows": [
            ("7.1", "Turn 1: 'My name is Liam.' — Turn 2 (same thread): 'What forms do I need?' (multi-turn test)",
             "Agent uses 'Liam' in Turn 2 without being re-told. thread_id must be reused between turns."),
            ("7.2", "Can you help me write my resignation letter?",
             "Politely declines (out of scope); explains it only handles onboarding topics; offers to redirect to HR."),
            ("7.3", "What is Acme's stock price today?",
             "Does not speculate; acknowledges it is outside scope; routes to HR general enquiries or relevant contact."),
            ("7.4", "I don't understand the difference between the PPO and HMO plans. Can you explain more simply?",
             "Patient plain-English re-explanation: PPO (any doctor, no referrals) vs HMO (GP referral required); encouraging tone."),
            ("7.5", "What if I miss the 30-day benefits enrolment window?",
             "States changes are only possible at Open Enrolment (November) or Qualifying Life Event; directs to benefits@acme.com."),
            ("7.6", "I have a question that I don't think you can answer.",
             "Encourages the question; if truly out of scope routes to HR: hr@acme.com / Ext. 5000; never dismissive."),
        ],
    },
]

GREY = RGBColor(0x57, 0x60, 0x6A)
HEADER_BG = "1F4E79"  # dark blue header rows


def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def add_table(doc, rows_data):
    col_widths = [Inches(0.4), Inches(3.5), Inches(3.1)]
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"

    # Header row
    hdr = table.rows[0]
    for i, text in enumerate(("No.", "Question", "Expected Behaviour")):
        cell = hdr.cells[i]
        cell.width = col_widths[i]
        set_cell_bg(cell, HEADER_BG)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.size = Pt(10)

    # Data rows
    for num, question, expected in rows_data:
        row = table.add_row()
        data = [num, question, expected]
        for i, text in enumerate(data):
            cell = row.cells[i]
            cell.width = col_widths[i]
            p = cell.paragraphs[0]
            run = p.add_run(text)
            run.font.size = Pt(10)

    doc.add_paragraph()  # spacer


def build():
    doc = Document()

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("AG_hr_onboarding_agent — Test Questions")
    run.bold = True
    run.font.size = Pt(20)

    sub1 = doc.add_paragraph()
    sub1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub1.add_run("IBM watsonx Orchestrate  ·  Acme Corporation HR Onboarding Agent")
    r.font.size = Pt(11)
    r.font.color.rgb = GREY

    sub2 = doc.add_paragraph()
    sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = sub2.add_run("7 categories · 40 test questions")
    r2.font.size = Pt(11)
    r2.font.color.rgb = GREY

    doc.add_paragraph()

    for cat in CATEGORIES:
        h = doc.add_heading(cat["title"], level=1)
        h.runs[0].font.size = Pt(14)

        note = doc.add_paragraph()
        r = note.add_run(cat["subtitle"])
        r.font.size = Pt(10)
        r.font.color.rgb = GREY

        add_table(doc, cat["rows"])

    # How to run section
    doc.add_heading("How to Run These Tests", level=1)
    instructions = [
        ("Option 1 — Bob (recommended)",
         "In the Bob chat, type:  Chat with AG_hr_onboarding_agent: <paste question here>"),
        ("Option 2 — watsonx Orchestrate UI",
         "Open AG_hr_onboarding_agent in the wxO web UI and type questions directly using the starter prompts or free text."),
        ("Option 3 — CLI",
         "source venv/bin/activate && orchestrate chat ask -n AG_hr_onboarding_agent \"<question>\" -r\n"
         "Note: -r shows the reasoning trace (which tools fired). On SaaS this may hang — prefer Option 1."),
        ("Multi-turn tests (question 7.1)",
         "Run Turn 1 first, then reuse the returned thread_id for Turn 2 so the agent retains context."),
    ]
    for label, detail in instructions:
        p = doc.add_paragraph()
        r_bold = p.add_run(label + ": ")
        r_bold.bold = True
        r_bold.font.size = Pt(11)
        r_rest = p.add_run(detail)
        r_rest.font.size = Pt(11)

    doc.save(str(OUTPUT))
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    build()
