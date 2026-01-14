"""
generate_test_data.py - Generate Test PDFs for CandidateCompass
===============================================================
Creates realistic government job descriptions and candidate resumes
for testing the application with various qualification scenarios.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from pathlib import Path


def create_job_description(output_path, job_data):
    """Generate a government job description PDF."""
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=12,
        alignment=TA_CENTER
    )
    story.append(Paragraph(job_data['title'], title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Agency & Department
    story.append(Paragraph(f"<b>Agency:</b> {job_data['agency']}", styles['Normal']))
    story.append(Paragraph(f"<b>Department:</b> {job_data['department']}", styles['Normal']))
    story.append(Paragraph(f"<b>Position Type:</b> {job_data['position_type']}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Summary
    story.append(Paragraph("<b>Position Summary</b>", styles['Heading2']))
    story.append(Paragraph(job_data['summary'], styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Required Education
    story.append(Paragraph("<b>Required Education</b>", styles['Heading2']))
    story.append(Paragraph(job_data['required_education'], styles['Normal']))
    story.append(Spacer(1, 0.1 * inch))

    # Required Skills
    story.append(Paragraph("<b>Required Skills (Must Have ALL)</b>", styles['Heading2']))
    for skill in job_data['required_skills']:
        story.append(Paragraph(f"• {skill}", styles['Normal']))
    story.append(Spacer(1, 0.1 * inch))

    # Required Any Of
    if job_data.get('required_any_of'):
        story.append(Paragraph("<b>Required Tools (Must Have at Least ONE)</b>", styles['Heading2']))
        for tool in job_data['required_any_of']:
            story.append(Paragraph(f"• {tool}", styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

    # Experience Levels
    if job_data.get('levels'):
        story.append(Paragraph("<b>Position Levels & Experience Requirements</b>", styles['Heading2']))
        for level, exp in zip(job_data['levels'], job_data['experience_required']):
            story.append(Paragraph(f"• <b>Level {level}:</b> {exp}+ years of relevant experience", styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

    # Duties
    story.append(Paragraph("<b>Key Responsibilities</b>", styles['Heading2']))
    for duty in job_data.get('duties', []):
        story.append(Paragraph(f"• {duty}", styles['Normal']))

    doc.build(story)
    print(f"✅ Created job description: {output_path.name}")


def create_resume(output_path, resume_data):
    """Generate a candidate resume PDF."""
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Header
    name_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='black',
        spaceAfter=6,
        alignment=TA_CENTER
    )
    story.append(Paragraph(resume_data['name'], name_style))
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    story.append(Paragraph(resume_data['contact'], contact_style))
    story.append(Spacer(1, 0.2 * inch))

    # Summary
    story.append(Paragraph("<b>PROFESSIONAL SUMMARY</b>", styles['Heading2']))
    story.append(Paragraph(resume_data['summary'], styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Education
    story.append(Paragraph("<b>EDUCATION</b>", styles['Heading2']))
    for edu in resume_data['education']:
        story.append(Paragraph(f"<b>{edu['degree']}</b>", styles['Normal']))
        story.append(Paragraph(f"{edu['institution']}, {edu['year']}", styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

    # Skills
    story.append(Paragraph("<b>SKILLS</b>", styles['Heading2']))
    story.append(Paragraph(resume_data['skills'], styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Work Experience
    story.append(Paragraph("<b>WORK EXPERIENCE</b>", styles['Heading2']))
    for job in resume_data['experience']:
        story.append(Paragraph(f"<b>{job['title']}</b>", styles['Normal']))
        story.append(Paragraph(f"{job['company']}, {job['dates']}", styles['Normal']))
        for responsibility in job['responsibilities']:
            story.append(Paragraph(f"• {responsibility}", styles['Normal']))
        story.append(Spacer(1, 0.15 * inch))

    # Certifications (if any)
    if resume_data.get('certifications'):
        story.append(Paragraph("<b>CERTIFICATIONS</b>", styles['Heading2']))
        for cert in resume_data['certifications']:
            story.append(Paragraph(f"• {cert}", styles['Normal']))

    doc.build(story)
    print(f"✅ Created resume: {output_path.name}")


# =============================================================================
# TEST GROUP 1: Entry-Level Administrative Assistant
# =============================================================================

def generate_test_group_1():
    """Generate Test Group 1: Entry-Level Administrative Assistant"""
    print("\n📋 Generating Test Group 1: Entry-Level Administrative Assistant...")

    output_dir = Path("test_data/test_group_1_entry_admin")

    # Job Description
    job_data = {
        'title': 'Administrative Assistant I-II',
        'agency': 'Department of General Services',
        'department': 'Administrative Services Division',
        'position_type': 'Full-Time, Permanent',
        'summary': 'Provides administrative support to the Administrative Services Division. Performs clerical duties including filing, data entry, scheduling, and customer service. Assists with budget tracking and maintains office supplies inventory.',
        'required_education': "High School Diploma or GED. Associate's degree preferred but not required.",
        'required_skills': [
            'Microsoft Office Suite (Word, Excel, Outlook)',
            'Data entry and record keeping',
            'Customer service',
            'Written and verbal communication'
        ],
        'required_any_of': [
            'QuickBooks',
            'SAP',
            'Oracle Financials'
        ],
        'levels': ['I', 'II'],
        'experience_required': [1, 3],
        'duties': [
            'Answer phones and direct calls to appropriate staff',
            'Maintain filing systems and office records',
            'Schedule meetings and maintain calendars',
            'Process expense reports and purchase orders',
            'Provide customer service to internal and external stakeholders'
        ]
    }

    create_job_description(output_dir / "job_admin_assistant_I_II.pdf", job_data)

    # Resume 1: QUALIFIED Level II - Perfect match with 4 years experience
    resume1 = {
        'name': 'Sarah Mitchell',
        'contact': 'sarah.mitchell@email.com | (555) 123-4567 | Springfield, USA',
        'summary': 'Detail-oriented administrative professional with 4 years of experience providing comprehensive support in government and corporate settings. Proficient in Microsoft Office Suite, QuickBooks, and customer service. Known for exceptional organizational skills and ability to manage multiple priorities.',
        'education': [
            {
                'degree': "Associate of Arts in Business Administration",
                'institution': 'Springfield Community College',
                'year': '2019'
            }
        ],
        'skills': 'Microsoft Office Suite (Word, Excel, PowerPoint, Outlook), QuickBooks, Data Entry, Customer Service, Written Communication, Verbal Communication, Filing Systems, Calendar Management, Budget Tracking',
        'experience': [
            {
                'title': 'Administrative Coordinator',
                'company': 'County Health Department',
                'dates': 'January 2021 - Present',
                'responsibilities': [
                    'Provide administrative support to department of 15 staff members',
                    'Manage calendars and schedule meetings for department heads',
                    'Process expense reports and purchase orders using QuickBooks',
                    'Maintain filing systems and electronic records for patient documentation',
                    'Answer multi-line phone system and direct calls to appropriate personnel'
                ]
            },
            {
                'title': 'Office Assistant',
                'company': 'Springfield Medical Group',
                'dates': 'May 2019 - December 2020',
                'responsibilities': [
                    'Performed data entry and maintained patient records',
                    'Provided customer service to patients and visitors',
                    'Managed office supplies inventory and placed orders',
                    'Created correspondence using Microsoft Word and Excel'
                ]
            }
        ],
        'certifications': [
            'Microsoft Office Specialist (MOS) - Excel, 2020'
        ]
    }

    create_resume(output_dir / "resume_qualified_level_II_sarah_mitchell.pdf", resume1)

    # Resume 2: QUALIFIED Level I - Entry level with 1.5 years
    resume2 = {
        'name': 'James Rodriguez',
        'contact': 'j.rodriguez@email.com | (555) 234-5678 | Springfield, USA',
        'summary': 'Motivated administrative professional with 1.5 years of experience in office support roles. Strong skills in Microsoft Office, data entry, and customer service. Eager to contribute to a government agency and grow professionally.',
        'education': [
            {
                'degree': 'High School Diploma',
                'institution': 'Springfield High School',
                'year': '2021'
            },
            {
                'degree': 'Certificate in Office Administration (in progress)',
                'institution': 'Springfield Community College',
                'year': 'Expected 2025'
            }
        ],
        'skills': 'Microsoft Office (Word, Excel, Outlook), Data Entry, Customer Service, Written Communication, Verbal Communication, Filing, SAP (basic knowledge)',
        'experience': [
            {
                'title': 'Administrative Assistant',
                'company': 'Green Valley Nonprofit Organization',
                'dates': 'June 2022 - Present',
                'responsibilities': [
                    'Answer phone calls and provide information to clients',
                    'Perform data entry and maintain donor database using Microsoft Excel',
                    'File documents and maintain organized filing system',
                    'Schedule appointments and meetings for executive director',
                    'Assist with event planning and coordination'
                ]
            },
            {
                'title': 'Receptionist (Part-time)',
                'company': 'Springfield Dental Clinic',
                'dates': 'January 2022 - May 2022',
                'responsibilities': [
                    'Greeted patients and provided excellent customer service',
                    'Answered phones and scheduled appointments',
                    'Maintained patient files and records'
                ]
            }
        ]
    }

    create_resume(output_dir / "resume_qualified_level_I_james_rodriguez.pdf", resume2)

    # Resume 3: EDGE CASE - Just meets Level I threshold (exactly 1 year)
    resume3 = {
        'name': 'Maria Chen',
        'contact': 'maria.chen@email.com | (555) 345-6789 | Springfield, USA',
        'summary': 'Recent graduate with exactly 1 year of administrative experience. Proficient in Microsoft Office Suite and passionate about public service. Quick learner with strong attention to detail.',
        'education': [
            {
                'degree': "Associate of Science in Business",
                'institution': 'Springfield Community College',
                'year': '2023'
            }
        ],
        'skills': 'Microsoft Office Suite (Word, Excel, PowerPoint, Outlook), Data Entry, Customer Service, Written Communication, Verbal Communication, Oracle Financials (training completed)',
        'experience': [
            {
                'title': 'Administrative Intern',
                'company': 'City Planning Department',
                'dates': 'January 2023 - January 2024 (12 months)',
                'responsibilities': [
                    'Provided administrative support to planning staff',
                    'Performed data entry using Microsoft Excel and Oracle Financials',
                    'Answered phones and directed calls to appropriate departments',
                    'Maintained filing systems and organized documents',
                    'Assisted with customer service inquiries from residents',
                    'Created meeting minutes and correspondence using Microsoft Word'
                ]
            }
        ]
    }

    create_resume(output_dir / "resume_edge_case_exactly_1yr_maria_chen.pdf", resume3)

    # Resume 4: EDGE CASE - Missing one required skill (no "customer service" mentioned)
    resume4 = {
        'name': 'David Park',
        'contact': 'david.park@email.com | (555) 456-7890 | Springfield, USA',
        'summary': 'Administrative professional with 3 years of back-office experience. Expert in Microsoft Office and data management. Strong technical skills and detail-oriented approach to work.',
        'education': [
            {
                'degree': 'High School Diploma',
                'institution': 'Lincoln High School',
                'year': '2019'
            }
        ],
        'skills': 'Microsoft Office Suite (Word, Excel, Outlook, PowerPoint), Data Entry, Record Keeping, Written Communication, Verbal Communication, QuickBooks, Filing Systems',
        'experience': [
            {
                'title': 'Data Entry Specialist',
                'company': 'Springfield Records Management',
                'dates': 'March 2021 - Present',
                'responsibilities': [
                    'Enter data into database systems with 99% accuracy',
                    'Maintain electronic and paper filing systems',
                    'Use Microsoft Excel to create reports and track data',
                    'Process invoices and expense reports using QuickBooks',
                    'Communicate with team members via email and written memos'
                ]
            },
            {
                'title': 'Office Clerk',
                'company': 'County Archives Department',
                'dates': 'June 2019 - February 2021',
                'responsibilities': [
                    'Organized and filed historical documents',
                    'Performed data entry for archival database',
                    'Created spreadsheets using Microsoft Excel',
                    'Maintained record keeping systems'
                ]
            }
        ]
    }

    create_resume(output_dir / "resume_edge_case_missing_customer_service_david_park.pdf", resume4)

    # Resume 5: UNQUALIFIED - Lacks education and only 0.5 years experience
    resume5 = {
        'name': 'Alex Thompson',
        'contact': 'alex.thompson@email.com | (555) 567-8901 | Springfield, USA',
        'summary': 'Recent high school graduate seeking entry-level administrative position. Basic computer skills and willingness to learn. Strong work ethic and punctual.',
        'education': [
            {
                'degree': 'High School Diploma',
                'institution': 'Washington High School',
                'year': '2024'
            }
        ],
        'skills': 'Microsoft Word, Microsoft Excel (basic), Email, Data Entry',
        'experience': [
            {
                'title': 'Retail Associate',
                'company': 'Springfield Department Store',
                'dates': 'June 2024 - Present (6 months)',
                'responsibilities': [
                    'Assist customers with product selection',
                    'Operate cash register',
                    'Stock shelves and maintain store organization',
                    'Process returns and exchanges'
                ]
            }
        ]
    }

    create_resume(output_dir / "resume_unqualified_insufficient_experience_alex_thompson.pdf", resume5)

    print(f"✅ Test Group 1 complete: 1 job + 5 resumes generated")


# =============================================================================
# TEST GROUP 2: Mid-Level IT Specialist
# =============================================================================

def generate_test_group_2():
    """Generate Test Group 2: Mid-Level IT Specialist"""
    print("\n💻 Generating Test Group 2: Mid-Level IT Specialist...")

    output_dir = Path("test_data/test_group_2_mid_it")

    # Job Description
    job_data = {
        'title': 'IT Specialist II-IV (Network Administration)',
        'agency': 'Department of Information Technology',
        'department': 'Network Infrastructure Division',
        'position_type': 'Full-Time, Permanent',
        'summary': 'Responsible for planning, implementing, and maintaining network infrastructure for government agency. Manages servers, network security, and provides technical support. Ensures system reliability, security, and performance optimization.',
        'required_education': "Bachelor's degree in Computer Science, Information Technology, or related field. Equivalent work experience may substitute on a year-for-year basis.",
        'required_skills': [
            'Network administration',
            'Windows Server',
            'Linux/Unix',
            'TCP/IP protocols',
            'Network security'
        ],
        'required_any_of': [
            'Cisco routers',
            'Juniper networks',
            'Fortinet firewalls',
            'Palo Alto firewalls'
        ],
        'levels': ['II', 'III', 'IV'],
        'experience_required': [3, 5, 7],
        'duties': [
            'Design, implement, and maintain network infrastructure',
            'Configure and manage routers, switches, and firewalls',
            'Monitor network performance and troubleshoot issues',
            'Implement security policies and access controls',
            'Maintain documentation for network configurations',
            'Provide technical support to end users and staff',
            'Participate in disaster recovery planning and testing'
        ]
    }

    create_job_description(output_dir / "job_it_specialist_II_IV.pdf", job_data)

    # Resume 1: QUALIFIED Level IV - Senior with 8 years + all certs
    resume1 = {
        'name': 'Michael Anderson',
        'contact': 'michael.anderson@email.com | (555) 111-2222 | Capital City, USA',
        'summary': 'Senior IT professional with 8 years of experience in network administration and infrastructure management. Expert in Windows Server, Linux, network security, and enterprise firewall solutions. Proven track record of implementing secure, scalable network solutions for government agencies.',
        'education': [
            {
                'degree': "Bachelor of Science in Computer Science",
                'institution': 'State University',
                'year': '2015'
            }
        ],
        'skills': 'Network Administration, Windows Server 2016/2019/2022, Linux (Ubuntu, CentOS, RHEL), Unix, TCP/IP Protocols, Network Security, Cisco Routers and Switches, Fortinet Firewalls, Palo Alto Firewalls, VMware, Active Directory, DNS, DHCP, VPN, IDS/IPS',
        'experience': [
            {
                'title': 'Senior Network Administrator',
                'company': 'State Department of Transportation',
                'dates': 'January 2020 - Present',
                'responsibilities': [
                    'Manage network infrastructure serving 500+ users across 10 locations',
                    'Configure and maintain Cisco routers, switches, and Fortinet firewalls',
                    'Implement network security policies including IDS/IPS and VPN solutions',
                    'Administer Windows Server 2019/2022 and Linux servers (CentOS, Ubuntu)',
                    'Design and deploy network segmentation using TCP/IP and VLAN configurations',
                    'Lead disaster recovery planning and conduct quarterly DR tests',
                    'Provide Tier 3 technical support and mentor junior IT staff'
                ]
            },
            {
                'title': 'Network Administrator',
                'company': 'County IT Department',
                'dates': 'June 2016 - December 2019',
                'responsibilities': [
                    'Administered network infrastructure including Cisco equipment and Palo Alto firewalls',
                    'Managed Windows Server 2016 environment and Active Directory',
                    'Implemented TCP/IP network protocols and security best practices',
                    'Monitored network performance using network management tools',
                    'Created and maintained network documentation and procedures'
                ]
            }
        ],
        'certifications': [
            'Cisco Certified Network Professional (CCNP), 2022',
            'CompTIA Security+, 2019',
            'Microsoft Certified: Windows Server Hybrid Administrator Associate, 2021'
        ]
    }

    create_resume(output_dir / "resume_qualified_level_IV_michael_anderson.pdf", resume1)

    # Resume 2: QUALIFIED Level III - 5 years with Bachelor's
    resume2 = {
        'name': 'Jennifer Lee',
        'contact': 'jennifer.lee@email.com | (555) 222-3333 | Capital City, USA',
        'summary': 'Network administrator with 5 years of hands-on experience managing enterprise networks. Strong background in Windows Server, Linux, and network security. Skilled in Cisco routing and Fortinet firewall administration.',
        'education': [
            {
                'degree': "Bachelor of Science in Information Technology",
                'institution': 'Tech State University',
                'year': '2018'
            }
        ],
        'skills': 'Network Administration, Windows Server 2016/2019, Linux (Ubuntu, Debian), TCP/IP Protocols, Network Security, Cisco Routers and Switches, Fortinet Firewalls, Active Directory, DNS, DHCP, VPN Configuration, Network Monitoring',
        'experience': [
            {
                'title': 'Network Administrator',
                'company': 'Regional Medical Center',
                'dates': 'March 2019 - Present',
                'responsibilities': [
                    'Administer network infrastructure for healthcare facility with 200+ users',
                    'Configure and maintain Cisco routers, switches, and Fortinet firewall appliances',
                    'Manage Windows Server 2019 environment including Active Directory and DNS',
                    'Implement network security measures to ensure HIPAA compliance',
                    'Troubleshoot TCP/IP networking issues and optimize network performance',
                    'Maintain Linux servers (Ubuntu) for specialized applications',
                    'Provide technical support and training to clinical and administrative staff'
                ]
            },
            {
                'title': 'IT Support Specialist',
                'company': 'City School District',
                'dates': 'June 2018 - February 2019',
                'responsibilities': [
                    'Provided desktop support and network troubleshooting',
                    'Assisted with network administration tasks under supervision',
                    'Configured workstations and managed Active Directory accounts'
                ]
            }
        ],
        'certifications': [
            'Cisco Certified Network Associate (CCNA), 2020',
            'CompTIA Network+, 2018'
        ]
    }

    create_resume(output_dir / "resume_qualified_level_III_jennifer_lee.pdf", resume2)

    # Resume 3: QUALIFIED Level II - 3.5 years, education substitution case
    resume3 = {
        'name': 'Robert Martinez',
        'contact': 'robert.martinez@email.com | (555) 333-4444 | Capital City, USA',
        'summary': 'Network administrator with 7 years of progressive IT experience. No formal degree but extensive hands-on experience equivalent to bachelor\'s degree plus 3 years. Proficient in Windows Server, Linux administration, and Cisco network equipment.',
        'education': [
            {
                'degree': 'Associate of Applied Science in Network Technology',
                'institution': 'Capital City Technical College',
                'year': '2016'
            }
        ],
        'skills': 'Network Administration, Windows Server 2012/2016/2019, Linux (CentOS, Red Hat), Unix, TCP/IP Protocols, Network Security, Cisco Routers and Switches, Juniper Networks, Active Directory, Group Policy, VPN, Network Troubleshooting',
        'experience': [
            {
                'title': 'Network Administrator',
                'company': 'State Housing Authority',
                'dates': 'January 2021 - Present',
                'responsibilities': [
                    'Manage network infrastructure for multi-site organization',
                    'Administer Windows Server 2019 environment and Active Directory',
                    'Configure Cisco switches and routers for network connectivity',
                    'Implement network security using Juniper firewalls and VPN solutions',
                    'Maintain Linux servers (CentOS) for file sharing and applications',
                    'Troubleshoot TCP/IP network issues and optimize performance',
                    'Create network documentation and standard operating procedures'
                ]
            },
            {
                'title': 'IT Technician',
                'company': 'County Library System',
                'dates': 'March 2017 - December 2020',
                'responsibilities': [
                    'Supported network administration tasks including switch configuration',
                    'Managed Windows Server 2012/2016 systems and Active Directory',
                    'Troubleshot network connectivity issues using TCP/IP protocols',
                    'Provided technical support to library staff and patrons',
                    'Assisted with Linux server maintenance and backups'
                ]
            }
        ],
        'certifications': [
            'CompTIA Network+, 2017',
            'CompTIA Security+, 2019'
        ]
    }

    create_resume(output_dir / "resume_qualified_level_II_education_sub_robert_martinez.pdf", resume3)

    # Resume 4: UNQUALIFIED - Has experience but missing required Linux/Unix skill
    resume4 = {
        'name': 'Emily White',
        'contact': 'emily.white@email.com | (555) 444-5555 | Capital City, USA',
        'summary': 'IT professional with 4 years of experience in Windows server administration and network support. Strong background in Microsoft technologies and Cisco networking. Seeking to expand skills in multi-platform environments.',
        'education': [
            {
                'degree': "Bachelor of Science in Information Systems",
                'institution': 'State College',
                'year': '2019'
            }
        ],
        'skills': 'Network Administration, Windows Server 2016/2019, TCP/IP Protocols, Network Security, Cisco Routers and Switches, Active Directory, Exchange Server, Group Policy, PowerShell, Fortinet Firewalls',
        'experience': [
            {
                'title': 'Windows Server Administrator',
                'company': 'Private Healthcare Company',
                'dates': 'July 2020 - Present',
                'responsibilities': [
                    'Administer Windows Server 2016/2019 infrastructure',
                    'Manage Active Directory, DNS, DHCP, and Group Policy',
                    'Configure Cisco network switches and Fortinet firewalls',
                    'Implement network security policies and access controls',
                    'Troubleshoot TCP/IP networking and connectivity issues',
                    'Provide technical support for server and network issues'
                ]
            },
            {
                'title': 'IT Support Specialist',
                'company': 'Manufacturing Company',
                'dates': 'May 2019 - June 2020',
                'responsibilities': [
                    'Provided desktop and network support',
                    'Assisted with Windows Server administration',
                    'Configured workstations and network connectivity'
                ]
            }
        ],
        'certifications': [
            'Microsoft Certified Solutions Associate (MCSA), 2020',
            'Cisco Certified Network Associate (CCNA), 2021'
        ]
    }

    create_resume(output_dir / "resume_unqualified_no_linux_emily_white.pdf", resume4)

    # Resume 5: UNQUALIFIED - Strong skills but only 2 years experience (below Level II)
    resume5 = {
        'name': 'Daniel Brown',
        'contact': 'daniel.brown@email.com | (555) 555-6666 | Capital City, USA',
        'summary': 'Emerging IT professional with 2 years of experience in network administration. Recent college graduate with strong academic background and hands-on lab experience. All required technical skills but limited professional experience.',
        'education': [
            {
                'degree': "Bachelor of Science in Network Engineering",
                'institution': 'Capital State University',
                'year': '2022'
            }
        ],
        'skills': 'Network Administration, Windows Server 2019/2022, Linux (Ubuntu, Kali, CentOS), Unix, TCP/IP Protocols, Network Security, Cisco Routers and Switches, Palo Alto Firewalls, Juniper Networks, Active Directory, Virtualization (VMware, Hyper-V)',
        'experience': [
            {
                'title': 'Junior Network Administrator',
                'company': 'Small Business IT Services',
                'dates': 'June 2022 - Present (2 years)',
                'responsibilities': [
                    'Assist with network administration for small business clients',
                    'Configure Cisco switches and routers under supervision',
                    'Manage Windows Server 2019 and Active Directory',
                    'Maintain Linux servers (Ubuntu) for various applications',
                    'Implement basic network security measures and Palo Alto firewall rules',
                    'Troubleshoot TCP/IP connectivity issues',
                    'Provide technical support to end users'
                ]
            }
        ],
        'certifications': [
            'Cisco Certified Network Associate (CCNA), 2022',
            'CompTIA Security+, 2023',
            'CompTIA Linux+, 2023'
        ]
    }

    create_resume(output_dir / "resume_unqualified_only_2yrs_daniel_brown.pdf", resume5)

    print(f"✅ Test Group 2 complete: 1 job + 5 resumes generated")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CandidateCompass Test Data Generator")
    print("=" * 70)

    generate_test_group_1()
    generate_test_group_2()

    print("\n" + "=" * 70)
    print("✅ Test data generation complete!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  • test_data/test_group_1_entry_admin/")
    print("    - 1 job description + 5 resumes")
    print("  • test_data/test_group_2_mid_it/")
    print("    - 1 job description + 5 resumes")
    print("\nNext: Run test groups through CandidateCompass to validate results.")
