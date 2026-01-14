"""
Anonymize government job postings by removing agency-specific references.
Creates sanitized versions suitable for demo purposes.
"""

import re
from pathlib import Path


def anonymize_job_text(text):
    """
    Remove or replace agency-specific information from job descriptions.

    Replacements:
    - TxDOT / Texas Department of Transportation → State Transportation Agency
    - Austin, TX / specific cities → State Capital
    - Tyler / other TX cities → Regional Office
    - Specific addresses → [Address Anonymized]
    - Specific dates → [Date]
    - Job posting numbers → [REQ-XXXXX]
    """

    # Replace agency names
    text = re.sub(r'TxDOT', 'State Transportation Agency', text, flags=re.IGNORECASE)
    text = re.sub(r'Texas Department of Transportation', 'State Transportation Agency', text, flags=re.IGNORECASE)
    text = re.sub(r'State of Texas', 'State Government', text)

    # Replace location-specific references
    text = re.sub(r'Austin,?\s*TX', 'State Capital', text, flags=re.IGNORECASE)
    text = re.sub(r'Austin\s*78\d{3}', 'State Capital', text, flags=re.IGNORECASE)
    text = re.sub(r'Tyler,?\s*TX', 'Regional Office', text, flags=re.IGNORECASE)
    text = re.sub(r'Tyler\s*75\d{3}', 'Regional Office', text, flags=re.IGNORECASE)

    # Replace specific addresses
    text = re.sub(r'\d{3,5}\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Boulevard|Blvd|Drive|Dr)[^\n]*', '[Address Anonymized]', text)

    # Replace specific divisions/districts
    text = re.sub(r'Bridge Division', 'Infrastructure Division', text)
    text = re.sub(r'Financial Management Division', 'Finance Division', text)
    text = re.sub(r'Tyler District', 'Regional District', text)
    text = re.sub(r'Stassney [Cc]ampus', 'State Campus', text)

    # Replace job requisition numbers
    text = re.sub(r'\(?\d{7,8}\)?', '[REQ-XXXXX]', text)

    # Replace specific dates
    text = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+20\d{2}', '[Date]', text)
    text = re.sub(r'(December|January)\s+\d{1,2},?\s+20\d{2}', '[Date]', text)

    # Replace state job codes
    text = re.sub(r'\b[A-Z]{1,2}\d{3,4}\b', '[JOB-CODE]', text)
    text = re.sub(r'State Job Code/s?:\s*\d{4}(/\d{4})*', 'State Job Code: [CLASSIFIED]', text)
    text = re.sub(r'State Job Title/s?:[^\n]+', 'State Job Title: [As Posted]', text)

    # Replace Texas-specific links
    text = re.sub(r'https?://[^\s]*texas\.gov[^\s]*', '[State HR Portal]', text)
    text = re.sub(r'www\.[^\s]*texas\.gov[^\s]*', '[State HR Portal]', text)

    # Replace ERS/benefits specific to Texas
    text = re.sub(r'ERS \(texas\.gov\)', 'State Employee Benefits Portal', text)
    text = re.sub(r'Benefits at a Glance \| ERS[^\)]*', 'State Benefits Portal', text)

    # Clean up any remaining Texas references
    text = re.sub(r'\bTexas\b', 'State', text)
    text = re.sub(r'\bTX\b', '', text)

    return text


def process_job_files():
    """Process all job files and create anonymized versions."""

    input_dir = Path("sample_data/generated/ActualJobs")
    output_dir = Path("sample_data/generated/AnonymizedJobs")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process only the main job description PDFs (skip .doc files which appear to be duplicates)
    job_files = [
        "TxDOT Data Analyst 1-5.pdf",
        "TxDOT Data Analyst 3-5 (1).pdf",
        "Business Analyst II-III.pdf",
        "Contract Specialist II, III, IV or V.pdf",
        "Administrative Assistant I, II, III, IV.pdf",
    ]

    # For PDF files, we'll create text extraction instructions
    # Since we can't directly edit PDFs, we'll create a mapping file

    job_mapping = {
        "TxDOT Data Analyst 1-5.pdf": {
            "anonymized_name": "Data Analyst I-V.pdf",
            "title": "Data Analyst I - V - Infrastructure Division",
            "description": "State Transportation Agency position for data analysis and research"
        },
        "TxDOT Data Analyst 3-5 (1).pdf": {
            "anonymized_name": "Data Analyst III-V.pdf",
            "title": "Data Analyst III - V - Infrastructure Division",
            "description": "Senior-level State Transportation Agency data analyst position"
        },
        "Business Analyst II-III.pdf": {
            "anonymized_name": "Business Analyst II-III.pdf",
            "title": "Business Analyst II-III - Finance Division",
            "description": "State agency business analyst for financial systems"
        },
        "Contract Specialist II, III, IV or V.pdf": {
            "anonymized_name": "Contract Specialist II-V.pdf",
            "title": "Contract Specialist II - V - Regional District",
            "description": "Government contract specialist for procurement and compliance"
        },
        "Administrative Assistant I, II, III, IV.pdf": {
            "anonymized_name": "Administrative Assistant I-IV.pdf",
            "title": "Administrative Assistant I - IV",
            "description": "State agency administrative support position"
        },
    }

    # Save mapping for use in the app
    import json
    with open(output_dir / "job_mapping.json", "w") as f:
        json.dump(job_mapping, f, indent=2)

    print(f"Created job mapping file at {output_dir / 'job_mapping.json'}")
    print(f"\nJob files to be used in demo:")
    for original, info in job_mapping.items():
        print(f"  - {info['title']}")

    return job_mapping


if __name__ == "__main__":
    mapping = process_job_files()
    print("\nAnonymization mapping created successfully!")
