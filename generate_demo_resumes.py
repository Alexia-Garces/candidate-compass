"""
Generate realistic demo resumes for government job screening workshop.

Creates candidates with varying qualification levels to demonstrate:
- Qualification gating (some qualified, some not)
- Level matching (Level I through V)
- Skill detection (government-specific skills)
- Education substitution (degree vs. experience)
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from pathlib import Path
import random

# Candidate profiles for Data Analyst positions
CANDIDATE_PROFILES = [
    {
        # QUALIFIED - Level V (Senior)
        "name": "Candidate A",
        "filename": "candidate_a_qualified_level5.pdf",
        "education": "Master of Science in Data Analytics, State University, 2018",
        "years_experience": 5,
        "skills": ["Tableau", "Power BI", "SQL", "Python", "data visualization", "dashboard development",
                   "stakeholder engagement", "government regulations", "report writing"],
        "experience_desc": [
            "Senior Data Analyst - State Transportation Agency (2021-Present)",
            "• Developed interactive Tableau dashboards for bridge inspection data serving 200+ stakeholders",
            "• Led data visualization projects analyzing $500M infrastructure budget",
            "• Collaborated with governmental officials to present findings to state legislature",
            "• Implemented SQL-based ETL processes for data warehouse modernization",
            "• Trained junior analysts on Power BI and data visualization best practices",
            "",
            "Data Analyst II - Regional Planning Organization (2019-2021)",
            "• Created SQL queries and Tableau reports for transportation planning data",
            "• Conducted stakeholder engagement sessions with 15+ local government agencies",
            "• Analyzed traffic data to support policy development and regulatory compliance"
        ],
        "certifications": ["Tableau Certified Data Analyst", "Microsoft Certified: Power BI Data Analyst"],
        "qualified": True,
        "level": "V"
    },
    {
        # QUALIFIED - Level III (Mid-level)
        "name": "Candidate B",
        "filename": "candidate_b_qualified_level3.pdf",
        "education": "Bachelor of Science in Computer Science, Tech University, 2021",
        "years_experience": 2,
        "skills": ["Tableau", "SQL", "Excel", "data analysis", "business analysis",
                   "technical documentation", "stakeholder management"],
        "experience_desc": [
            "Data Analyst - County Health Department (2022-Present)",
            "• Developed Tableau dashboards for public health data tracking COVID-19 metrics",
            "• Wrote SQL queries to extract and analyze data from multiple data sources",
            "• Created technical documentation for data processes and Excel-based reports",
            "• Collaborated with cross-functional teams including epidemiologists and administrators",
            "",
            "Junior Data Analyst - Private Healthcare Company (2021-2022)",
            "• Performed data analysis using Excel and SQL for operational reports",
            "• Assisted in dashboard development and data visualization projects"
        ],
        "certifications": [],
        "qualified": True,
        "level": "III"
    },
    {
        # QUALIFIED - Level II (Entry+)
        "name": "Candidate C",
        "filename": "candidate_c_qualified_level2.pdf",
        "education": "Bachelor of Arts in Statistics, State College, 2023",
        "years_experience": 1,
        "skills": ["SQL", "Tableau", "Excel", "data analysis", "report writing"],
        "experience_desc": [
            "Data Analyst - City Planning Department (2023-Present)",
            "• Analyzed data using SQL and created Tableau visualizations for planning reports",
            "• Developed Excel-based reports for city council presentations",
            "• Assisted senior analysts with data quality assessments and report writing",
            "• Participated in stakeholder meetings with community members and officials"
        ],
        "certifications": [],
        "qualified": True,
        "level": "II"
    },
    {
        # QUALIFIED - Level I (Entry) - NO DEGREE but experience substitution
        "name": "Candidate D",
        "filename": "candidate_d_qualified_level1_substitution.pdf",
        "education": "Some college coursework, no degree",
        "years_experience": 5,  # Substitutes for Bachelor's
        "skills": ["SQL", "Qlik", "Excel", "data analysis", "technical analysis", "government regulations"],
        "experience_desc": [
            "Operations Analyst - State Revenue Department (2019-Present)",
            "• 5 years of data analysis experience using SQL, Qlik, and Excel",
            "• Created data visualizations and reports for tax revenue analysis",
            "• Expertise in government regulations and compliance reporting",
            "• Conducted technical analysis of financial data for state auditors",
            "• Built Qlik dashboards for budget tracking and forecasting",
            "",
            "Note: 5+ years of relevant work experience qualifies as Bachelor's degree equivalent",
            "under state government substitution rules (4 years experience = Bachelor's degree)"
        ],
        "certifications": [],
        "qualified": True,
        "level": "I",
        "note": "Qualifies via education substitution"
    },
    {
        # DISQUALIFIED - Missing required skills (no Tableau/Power BI/Qlik)
        "name": "Candidate E",
        "filename": "candidate_e_disqualified_missing_skills.pdf",
        "education": "Bachelor of Science in Mathematics, University, 2020",
        "years_experience": 3,
        "skills": ["Python", "R", "SQL", "Excel", "data analysis", "machine learning"],  # Has SQL but missing Tableau/Power BI/Qlik!
        "experience_desc": [
            "Data Scientist - Tech Startup (2020-Present)",
            "• Developed machine learning models using Python and R",
            "• Performed statistical analysis and data mining on customer data using SQL",
            "• Created Excel reports and Python-based visualizations",
            "• No experience with enterprise BI platforms",
            "• Limited exposure to government sector or public sector work"
        ],
        "certifications": [],
        "qualified": False,
        "reason": "Missing required visualization tools (Tableau, Power BI, or Qlik)"
    },
    {
        # DISQUALIFIED - Insufficient experience AND no degree
        "name": "Candidate F",
        "filename": "candidate_f_disqualified_education.pdf",
        "education": "High school diploma, some college coursework",
        "years_experience": 2,  # Not enough for substitution (needs 4)
        "skills": ["Excel", "SQL", "Tableau", "data analysis"],
        "experience_desc": [
            "Data Entry Specialist - Private Company (2022-Present)",
            "• 2 years of data entry and basic Excel analysis",
            "• Created simple Tableau charts from templates",
            "• Basic SQL query writing for data extraction",
            "• Limited analytical experience and no formal degree"
        ],
        "certifications": [],
        "qualified": False,
        "reason": "Does not meet education requirement (needs Bachelor's OR 4+ years experience, has only 2 years)"
    },
    {
        # QUALIFIED - Level IV (Senior mid-level)
        "name": "Candidate G",
        "filename": "candidate_g_qualified_level4.pdf",
        "education": "Bachelor of Science in Information Systems, State University, 2019",
        "years_experience": 4,
        "skills": ["Tableau", "Power BI", "SQL", "Python", "data warehouse", "ETL",
                   "dashboard development", "stakeholder engagement", "public sector",
                   "process improvement", "requirements gathering"],
        "experience_desc": [
            "Senior Data Analyst - State Education Department (2020-Present)",
            "• 4 years of government experience analyzing statewide education data",
            "• Developed complex Tableau and Power BI dashboards for department leadership",
            "• Led requirements gathering sessions with stakeholders across 20+ school districts",
            "• Designed and implemented SQL-based ETL processes for data warehouse",
            "• Managed data visualization projects with $200K budget",
            "• Presented findings to state board of education and legislative committees",
            "",
            "Data Analyst - Public Charter School Network (2019-2020)",
            "• Created Tableau reports for student performance and budget tracking",
            "• Collaborated with school administrators on process improvement initiatives"
        ],
        "certifications": ["Tableau Desktop Specialist", "PMP (Project Management Professional)"],
        "qualified": True,
        "level": "IV"
    },
    {
        # QUALIFIED - Level III with strong government background
        "name": "Candidate H",
        "filename": "candidate_h_qualified_level3_gov.pdf",
        "education": "Bachelor of Public Administration, State College, 2020",
        "years_experience": 3,
        "skills": ["Tableau", "SQL", "Excel", "Power BI", "data analysis", "policy development",
                   "government regulations", "compliance", "stakeholder management",
                   "governmental officials", "public records", "budget management"],
        "experience_desc": [
            "Data & Policy Analyst - State Budget Office (2021-Present)",
            "• 3 years analyzing state budget data using Tableau, SQL, and Excel",
            "• Created Power BI dashboards for legislative budget tracking ($10B+ budget)",
            "• Collaborated with governmental officials and agency directors on policy development",
            "• Expertise in government regulations, compliance reporting, and public records laws",
            "• Managed stakeholder engagement with 25+ state agencies",
            "• Conducted budget analysis and financial reporting for state legislature",
            "",
            "Budget Analyst Intern - City Finance Department (2020-2021)",
            "• Performed data analysis for municipal budget preparation",
            "• Created Excel reports and Tableau visualizations for city council"
        ],
        "certifications": ["Certified Government Financial Manager (CGFM)"],
        "qualified": True,
        "level": "III"
    },
]


def create_resume_pdf(profile, output_dir):
    """Generate a realistic PDF resume from profile data."""

    filepath = output_dir / profile["filename"]
    doc = SimpleDocTemplate(str(filepath), pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#333333',
        spaceAfter=6
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor='#333333',
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor='#333333'
    )

    story = []

    # Name (anonymized as "Candidate X")
    story.append(Paragraph(profile["name"], title_style))
    story.append(Spacer(1, 0.2*inch))

    # Contact (will be anonymized by app)
    story.append(Paragraph(f"Email: {profile['name'].lower().replace(' ', '.')}@email.com", body_style))
    story.append(Paragraph("Phone: (555) 123-4567", body_style))
    story.append(Spacer(1, 0.2*inch))

    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    story.append(Paragraph(profile["education"], body_style))
    story.append(Spacer(1, 0.15*inch))

    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
    for line in profile["experience_desc"]:
        if line:
            story.append(Paragraph(line, body_style))
        else:
            story.append(Spacer(1, 0.1*inch))
    story.append(Spacer(1, 0.15*inch))

    # Skills
    story.append(Paragraph("SKILLS & COMPETENCIES", heading_style))
    skills_text = ", ".join(profile["skills"])
    story.append(Paragraph(skills_text, body_style))
    story.append(Spacer(1, 0.15*inch))

    # Certifications
    if profile["certifications"]:
        story.append(Paragraph("CERTIFICATIONS", heading_style))
        for cert in profile["certifications"]:
            story.append(Paragraph(f"• {cert}", body_style))

    # Build PDF
    doc.build(story)
    print(f"✅ Created: {profile['filename']} - {profile.get('note', profile['level'] if profile['qualified'] else 'DISQUALIFIED')}")


def main():
    """Generate all demo resumes."""
    output_dir = Path("sample_data/generated/DemoResumes")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n🚀 Generating Demo Resumes for Workshop...\n")

    qualified_count = 0
    disqualified_count = 0

    for profile in CANDIDATE_PROFILES:
        create_resume_pdf(profile, output_dir)
        if profile["qualified"]:
            qualified_count += 1
        else:
            disqualified_count += 1

    print(f"\n✅ Generated {len(CANDIDATE_PROFILES)} demo resumes:")
    print(f"   • {qualified_count} QUALIFIED candidates (Levels I-V)")
    print(f"   • {disqualified_count} DISQUALIFIED candidates (missing requirements)")
    print(f"\n📁 Location: {output_dir}")

    # Generate summary
    print("\n📊 Candidate Summary:")
    print("-" * 60)
    for profile in CANDIDATE_PROFILES:
        status = f"✅ QUALIFIED (Level {profile['level']})" if profile['qualified'] else f"❌ DISQUALIFIED"
        if not profile['qualified']:
            status += f" - {profile['reason']}"
        if profile.get('note'):
            status += f" - {profile['note']}"
        print(f"{profile['name']}: {status}")

    print("\n" + "="*60)
    print("🎯 Workshop Demo Flow:")
    print("="*60)
    print("1. Load these resumes with Data Analyst I-V job")
    print("2. Show 6 QUALIFIED candidates (A, B, C, D, G, H)")
    print("3. Show 2 DISQUALIFIED candidates (E, F)")
    print("4. Demonstrate:")
    print("   - Qualification gating (education + skills checks)")
    print("   - Level matching (I, II, III, IV, V)")
    print("   - Education substitution (Candidate D)")
    print("   - Government skills detection")
    print("   - Ranking within levels")
    print("="*60)


if __name__ == "__main__":
    main()
