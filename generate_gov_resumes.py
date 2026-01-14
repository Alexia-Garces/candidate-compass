"""
Generate realistic government sector candidate resumes for demo.
Creates resumes with varying qualification levels for Data Analyst, Business Analyst, and Contract Specialist roles.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from pathlib import Path
import random


# Resume templates for different roles and levels
RESUME_TEMPLATES = {
    "data_analyst_qualified_l3": {
        "name": "[NAME REDACTED]",
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "summary": "Data Analyst with 2.5 years of experience in government transportation data analysis, specializing in Tableau dashboards, SQL database queries, and Power BI reporting. Proven track record of translating complex data into actionable insights for stakeholders.",
        "education": "Bachelor of Science in Statistics, State University, 2021",
        "experience": [
            {
                "title": "Data Analyst II",
                "org": "Regional Transportation Authority",
                "duration": "2022 - Present (2.5 years)",
                "bullets": [
                    "Developed 15+ Tableau dashboards for infrastructure performance monitoring, serving 30+ stakeholders",
                    "Wrote complex SQL queries to extract and analyze bridge inspection data from 5,000+ records",
                    "Created Power BI reports for executive leadership, reducing report generation time by 60%",
                    "Collaborated with cross-functional teams including engineers, procurement, and finance divisions",
                    "Ensured data quality and compliance with state data governance policies"
                ]
            },
            {
                "title": "Junior Data Analyst",
                "org": "Municipal Planning Department",
                "duration": "2021 - 2022 (1 year)",
                "bullets": [
                    "Analyzed transportation survey data using Excel and basic SQL queries",
                    "Assisted senior analysts in data visualization and report preparation",
                    "Maintained department databases and ensured data accuracy"
                ]
            }
        ],
        "skills": "Tableau, Power BI, SQL, Excel, Python, Data Visualization, Statistical Analysis, Dashboard Development, Stakeholder Management, Government Reporting",
        "certifications": "Tableau Desktop Specialist (2023)"
    },

    "data_analyst_qualified_l2": {
        "name": "[NAME REDACTED]",
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "summary": "Entry-level Data Analyst with 1 year of experience supporting transportation data projects. Proficient in Tableau, SQL, and Excel with strong analytical skills and eagerness to learn.",
        "education": "Bachelor of Arts in Information Systems, State College, 2023",
        "experience": [
            {
                "title": "Data Analyst",
                "org": "State Highway Safety Office",
                "duration": "2023 - Present (1 year)",
                "bullets": [
                    "Created Tableau visualizations for crash data analysis serving 15+ stakeholders",
                    "Wrote SQL queries to extract data from traffic safety databases",
                    "Assisted in preparing quarterly reports for state and federal agencies",
                    "Used Excel for data cleaning and preliminary analysis",
                    "Participated in cross-functional team meetings with engineers and policy staff"
                ]
            }
        ],
        "skills": "Tableau, SQL, Excel, Data Analysis, Data Visualization, Report Writing, Team Collaboration",
        "certifications": "None"
    },

    "data_analyst_unqualified_no_tools": {
        "name": "[NAME REDACTED]",
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "summary": "Recent graduate with strong analytical skills and passion for data. Seeking entry-level data analyst position to apply academic knowledge in real-world applications.",
        "education": "Bachelor of Science in Mathematics, State University, 2024",
        "experience": [
            {
                "title": "Student Research Assistant",
                "org": "University Statistics Lab",
                "duration": "2023 - 2024 (1 year)",
                "bullets": [
                    "Conducted statistical analysis using R and SPSS for academic research projects",
                    "Assisted professors with data collection and preliminary analysis",
                    "Created charts and graphs using Excel for research presentations",
                    "Collaborated with graduate students on research papers"
                ]
            }
        ],
        "skills": "R, SPSS, Excel, Statistical Analysis, Research Methods, Data Collection",
        "certifications": "None"
    },

    "business_analyst_qualified_l3": {
        "name": "[NAME REDACTED]",
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "summary": "Business Analyst with 4 years of experience in government financial systems analysis, specializing in Tableau reporting, business process improvement, and stakeholder requirements gathering. Proven ability to bridge technical and business teams.",
        "education": "Master of Business Administration (MBA), State University, 2020\nBachelor of Science in Computer Science, 2018",
        "experience": [
            {
                "title": "Business Analyst III",
                "org": "State Finance Department",
                "duration": "2021 - Present (4 years)",
                "bullets": [
                    "Led business analysis for financial management system upgrade serving 200+ state employees",
                    "Developed 25+ Tableau dashboards for budget tracking and expenditure reporting",
                    "Gathered requirements from 30+ stakeholders across multiple divisions",
                    "Created detailed technical specifications and process flow diagrams",
                    "Conducted user acceptance testing and training for new financial applications",
                    "Ensured compliance with state procurement regulations and data security policies"
                ]
            },
            {
                "title": "Business Analyst II",
                "org": "Regional Government Services",
                "duration": "2020 - 2021 (1 year)",
                "bullets": [
                    "Analyzed business processes and recommended improvements using SQL and Excel",
                    "Created status reports and presentations for executive leadership",
                    "Facilitated workshops with stakeholders to document business requirements"
                ]
            }
        ],
        "skills": "Tableau, Business Analysis, SQL, Excel, Requirements Gathering, Stakeholder Management, Process Improvement, Technical Documentation, ETL, Project Management, Government Compliance",
        "certifications": "Tableau Certified Associate (2022), PMP (2023)"
    },

    "business_analyst_unqualified_low_exp": {
        "name": "[NAME REDACTED]",
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "summary": "Business Analyst with 1.5 years of experience in private sector consulting. Seeking to transition skills to public sector work.",
        "education": "Bachelor of Business Administration, Private University, 2022",
        "experience": [
            {
                "title": "Junior Business Analyst",
                "org": "Tech Consulting Firm",
                "duration": "2023 - Present (1.5 years)",
                "bullets": [
                    "Analyzed client business processes and documented requirements",
                    "Created PowerPoint presentations for client deliverables",
                    "Assisted senior analysts with data analysis using Excel",
                    "Participated in client meetings and stakeholder interviews"
                ]
            }
        ],
        "skills": "Business Analysis, Excel, PowerPoint, Requirements Documentation, Stakeholder Communication",
        "certifications": "None"
    },

    "contract_specialist_qualified_l4": {
        "name": "[NAME REDACTED]",
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "summary": "Contract Specialist with 5 years of experience in government procurement and contract administration. Expert in federal and state procurement regulations, contract negotiations, and vendor management.",
        "education": "Bachelor of Science in Business Administration - Finance, State University, 2018",
        "experience": [
            {
                "title": "Contract Specialist IV",
                "org": "State Procurement Office",
                "duration": "2021 - Present (4 years)",
                "bullets": [
                    "Managed $50M+ portfolio of contracts for transportation infrastructure projects",
                    "Developed, reviewed, and negotiated complex contracts ensuring compliance with state and federal procurement regulations",
                    "Conducted vendor performance evaluations and resolved contract disputes",
                    "Interpreted federal acquisition regulations (FAR) and state statutes to ensure legal compliance",
                    "Collaborated with legal staff, program managers, and governmental officials on contract matters",
                    "Monitored contractor insurance certificates and fiscal documentation",
                    "Prepared bid proposals, conducted pre-construction meetings, and managed change orders",
                    "Served as subject matter expert on contract administration for departmental staff"
                ]
            },
            {
                "title": "Contract Specialist II",
                "org": "Regional Government Agency",
                "duration": "2019 - 2021 (2 years)",
                "bullets": [
                    "Prepared contract documents, amendments, and conditional award notices",
                    "Assisted with monitoring contractor compliance with regulations",
                    "Maintained contract files and documentation for audit purposes",
                    "Coordinated start-work dates and ensured materials availability"
                ]
            }
        ],
        "skills": "Contract Administration, Procurement, Compliance, Federal Regulations, State Regulations, Contract Negotiations, Vendor Management, Policy Development, Legal Review, Risk Management, Government Contracting",
        "certifications": "Certified Professional Public Buyer (CPPB), 2022"
    },

    "contract_specialist_marginal": {
        "name": "[NAME REDACTED]",
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "summary": "Administrative professional with 6 years of experience in contract coordination and bookkeeping. Strong attention to detail and experience supporting procurement processes.",
        "education": "Associate Degree in Business, Community College, 2017",
        "experience": [
            {
                "title": "Contract Coordinator",
                "org": "Private Construction Company",
                "duration": "2018 - Present (6 years)",
                "bullets": [
                    "Coordinated contract paperwork and document filing for construction projects",
                    "Maintained contract databases and tracking spreadsheets",
                    "Processed invoices and payment requests",
                    "Communicated with vendors regarding contract requirements",
                    "Assisted project managers with contract administration tasks"
                ]
            }
        ],
        "skills": "Contract Coordination, Document Management, Excel, Bookkeeping, Vendor Communication, Administrative Support",
        "certifications": "None"
    },
}


def generate_resume_pdf(template_key, output_path):
    """Generate a PDF resume from template."""
    template = RESUME_TEMPLATES[template_key]

    doc = SimpleDocTemplate(str(output_path), pagesize=letter,
                          leftMargin=0.75*inch, rightMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                fontSize=16, textColor=colors.HexColor('#333333'),
                                spaceAfter=6)

    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'],
                                  fontSize=12, textColor=colors.HexColor('#E31937'),
                                  spaceAfter=6, spaceBefore=12)

    # Name
    story.append(Paragraph(template['name'], title_style))
    story.append(Paragraph(f"{template['email']} | {template['phone']}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    story.append(Paragraph(template['summary'], styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    story.append(Paragraph(template['education'], styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
    for exp in template['experience']:
        story.append(Paragraph(f"<b>{exp['title']}</b> | {exp['org']}", styles['Normal']))
        story.append(Paragraph(f"<i>{exp['duration']}</i>", styles['Normal']))
        story.append(Spacer(1, 0.05*inch))

        for bullet in exp['bullets']:
            story.append(Paragraph(f"• {bullet}", styles['Normal']))

        story.append(Spacer(1, 0.1*inch))

    # Skills
    story.append(Paragraph("TECHNICAL SKILLS", heading_style))
    story.append(Paragraph(template['skills'], styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # Certifications
    story.append(Paragraph("CERTIFICATIONS", heading_style))
    story.append(Paragraph(template['certifications'], styles['Normal']))

    doc.build(story)
    print(f"✅ Generated: {output_path.name}")


def main():
    """Generate all demo resumes."""
    output_dir = Path("sample_data/generated/DemoResumes")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating government sector demo resumes...\n")

    # Generate resumes for each template
    resumes_generated = []
    for idx, (template_key, template_data) in enumerate(RESUME_TEMPLATES.items()):
        filename = f"candidate_{idx+1}_{template_key}.pdf"
        output_path = output_dir / filename
        generate_resume_pdf(template_key, output_path)
        resumes_generated.append({
            "file": filename,
            "template": template_key,
            "expected_qualification": "Qualified" if "qualified" in template_key else "Marginal/Unqualified"
        })

    print(f"\n✅ Generated {len(resumes_generated)} demo resumes in {output_dir}")
    print("\nResume Breakdown:")
    print("  Data Analyst Qualified (Level III): 1")
    print("  Data Analyst Qualified (Level II): 1")
    print("  Data Analyst Unqualified (No Tools): 1")
    print("  Business Analyst Qualified (Level III): 1")
    print("  Business Analyst Unqualified (Low Experience): 1")
    print("  Contract Specialist Qualified (Level IV): 1")
    print("  Contract Specialist Marginal (No Degree): 1")
    print(f"\nTotal: {len(resumes_generated)} candidates")

    return resumes_generated


if __name__ == "__main__":
    resumes = main()
