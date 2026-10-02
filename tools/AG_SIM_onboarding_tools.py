from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel
from typing import List


class OnboardingChecklistItem(BaseModel):
    task: str
    completed: bool
    notes: str


class OnboardingChecklist(BaseModel):
    employee_name: str
    checklist: List[OnboardingChecklistItem]
    summary: str


class PaperworkGuide(BaseModel):
    form_name: str
    description: str
    submission_method: str
    deadline: str
    contact: str


class ContactInfo(BaseModel):
    team: str
    email: str
    phone: str
    scope: str


@tool(permission=ToolPermission.READ_ONLY)
def AG_SIM_get_required_paperwork() -> List[PaperworkGuide]:
    """Return the list of required onboarding paperwork with submission details.

    Returns:
        List[PaperworkGuide]: Each required form with description, submission method, deadline, and contact.
    """
    return [
        PaperworkGuide(
            form_name="Form W-4 (Federal Tax Withholding)",
            description="Tells the company how much federal income tax to withhold from your pay.",
            submission_method="Download from hr.acme.internal/forms/w4, complete, and email to payroll@acme.com or drop off at HR reception (Level 2).",
            deadline="Within first 3 business days",
            contact="payroll@acme.com | Ext. 5100",
        ),
        PaperworkGuide(
            form_name="I-9 Employment Eligibility Verification",
            description="Verifies your identity and right to work in the US. Original documents must be presented in person.",
            submission_method="Bring original identity documents to HR reception on Day 1.",
            deadline="Day 1",
            contact="hr@acme.com | Ext. 5000",
        ),
        PaperworkGuide(
            form_name="Non-Disclosure Agreement (NDA)",
            description="Covers trade secrets, client information, and proprietary technology. Must be signed before or on Day 1.",
            submission_method="DocuSign link sent to your personal email before start date. Sign electronically.",
            deadline="Day 1 (ideally before start date)",
            contact="legal@acme.com | Ext. 6000",
        ),
        PaperworkGuide(
            form_name="Equipment Request Form",
            description="Specifies your laptop, monitors, peripherals, and any mobile device needs so IT can provision within 48 hours.",
            submission_method="Complete online at it.acme.internal/equipment-request.",
            deadline="End of Day 1",
            contact="helpdesk@acme.com | Ext. 4000",
        ),
        PaperworkGuide(
            form_name="Direct Deposit / Payroll Setup",
            description="Provides your bank details for bi-weekly direct deposit (every other Friday).",
            submission_method="Enter bank details in the Payroll Portal at payroll.acme.internal.",
            deadline="Within first 3 business days",
            contact="payroll@acme.com | Ext. 5100",
        ),
        PaperworkGuide(
            form_name="Benefits Enrolment",
            description="Elect your health, dental, vision, 401(k), and other benefits. Must be done within 30 days of hire.",
            submission_method="Log in to benefits.acme.internal and complete 'New Hire Enrolment'.",
            deadline="Within 30 days of hire date",
            contact="benefits@acme.com | Ext. 5200",
        ),
        PaperworkGuide(
            form_name="IT Acceptable Use Policy Acknowledgement",
            description="Confirms you have read and agree to Acme's IT and data security policies.",
            submission_method="Sign electronically via the IT Portal at it.acme.internal.",
            deadline="Within first 3 business days",
            contact="helpdesk@acme.com | Ext. 4000",
        ),
        PaperworkGuide(
            form_name="Employee Handbook Acknowledgement",
            description="Confirms you have read and agree to the Employee Handbook, including the Code of Conduct.",
            submission_method="DocuSign link sent to your work email on Day 1.",
            deadline="Within first 3 business days",
            contact="hr@acme.com | Ext. 5000",
        ),
    ]


@tool(permission=ToolPermission.READ_ONLY)
def AG_SIM_get_hr_contacts() -> List[ContactInfo]:
    """Return the directory of HR and support contacts for common employee enquiries.

    Returns:
        List[ContactInfo]: Team name, email, phone, and scope of support for each HR contact.
    """
    return [
        ContactInfo(
            team="HR General Enquiries",
            email="hr@acme.com",
            phone="Ext. 5000 | +1 (415) 555-0100",
            scope="General HR questions, policies, employment verification, probation reviews.",
        ),
        ContactInfo(
            team="Payroll",
            email="payroll@acme.com",
            phone="Ext. 5100",
            scope="Salary, direct deposit, tax forms, pay slips, expense reimbursements.",
        ),
        ContactInfo(
            team="Benefits Team",
            email="benefits@acme.com",
            phone="Ext. 5200 | +1 (415) 555-0200",
            scope="Health, dental, vision, 401(k), life insurance, EAP, wellness benefits, enrolment queries.",
        ),
        ContactInfo(
            team="IT Helpdesk",
            email="helpdesk@acme.com",
            phone="Ext. 4000",
            scope="Laptop setup, software access, account provisioning, VPN, security incidents.",
        ),
        ContactInfo(
            team="Legal Team",
            email="legal@acme.com",
            phone="Ext. 6000",
            scope="NDA questions, contract queries, intellectual property, legal compliance.",
        ),
        ContactInfo(
            team="Facilities",
            email="facilities@acme.com",
            phone="Ext. 3000",
            scope="Building access, parking, desk allocation, office supplies.",
        ),
        ContactInfo(
            team="Ethics Hotline",
            email="ethics@acme.com",
            phone="1-800-555-0199",
            scope="Confidential reporting of code-of-conduct violations, fraud, or harassment.",
        ),
        ContactInfo(
            team="HR Business Partner",
            email="hr-bp@acme.com",
            phone="See your welcome email for your assigned HRBP",
            scope="Escalated HR issues, performance management, team conflicts, organisational changes.",
        ),
        ContactInfo(
            team="Learning & Development",
            email="ld@acme.com",
            phone="Ext. 5300",
            scope="Training budget, LinkedIn Learning, tuition reimbursement, mentoring programme.",
        ),
    ]


@tool(permission=ToolPermission.READ_ONLY)
def AG_SIM_generate_onboarding_checklist(employee_name: str) -> OnboardingChecklist:
    """Generate a personalised onboarding checklist for a new employee.

    Args:
        employee_name (str): The full name of the new employee.
    Returns:
        OnboardingChecklist: A structured checklist with all required onboarding tasks, their completion status, and a summary.
    """
    checklist_items = [
        OnboardingChecklistItem(task="Sign Non-Disclosure Agreement (NDA)", completed=False, notes="DocuSign link sent to personal email — must be signed on or before Day 1."),
        OnboardingChecklistItem(task="Present I-9 documents at HR reception", completed=False, notes="Bring original identity/work-authorisation documents to Level 2 on Day 1."),
        OnboardingChecklistItem(task="Complete Form W-4 (federal tax withholding)", completed=False, notes="Download from hr.acme.internal/forms/w4 and submit to payroll@acme.com."),
        OnboardingChecklistItem(task="Set up direct deposit via Payroll Portal", completed=False, notes="Log in to payroll.acme.internal and enter your bank details."),
        OnboardingChecklistItem(task="Submit Equipment Request Form", completed=False, notes="Complete at it.acme.internal/equipment-request by end of Day 1."),
        OnboardingChecklistItem(task="Activate Acme SSO account and Microsoft 365", completed=False, notes="Activation link sent to personal email before start date."),
        OnboardingChecklistItem(task="Complete Benefits Enrolment", completed=False, notes="Must be done within 30 days — log in to benefits.acme.internal."),
        OnboardingChecklistItem(task="Sign IT Acceptable Use Policy", completed=False, notes="Sign electronically at it.acme.internal."),
        OnboardingChecklistItem(task="Sign Employee Handbook Acknowledgement", completed=False, notes="DocuSign link sent to work email on Day 1."),
        OnboardingChecklistItem(task="Complete Security Awareness & Data Protection training", completed=False, notes="~2 hours online — complete by end of Day 2. Link in Confluence."),
        OnboardingChecklistItem(task="Meet your Peer Buddy (assigned by HR on Day 1)", completed=False, notes="Your buddy is your go-to for informal questions during your first 30 days."),
        OnboardingChecklistItem(task="Schedule 1:1 with your direct manager", completed=False, notes="First 1:1 is on Day 1 at 3:00 PM. Weekly cadence recommended thereafter."),
        OnboardingChecklistItem(task="Day 30 check-in with manager", completed=False, notes="Review onboarding progress and set initial OKRs."),
        OnboardingChecklistItem(task="Day 90 probation review with manager", completed=False, notes="Formal review to confirm permanent employment status."),
    ]

    summary = (
        f"Onboarding checklist generated for {employee_name}. "
        f"There are {len(checklist_items)} tasks to complete. "
        "Critical Day 1 items: NDA, I-9, Equipment Request, SSO activation. "
        "Benefits enrolment must be completed within 30 days. "
        "All paperwork should be submitted within the first 3 business days."
    )

    return OnboardingChecklist(
        employee_name=employee_name,
        checklist=checklist_items,
        summary=summary,
    )
