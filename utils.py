"""
utils.py — CandidateCompass Utilities
======================================
Navigate Talent, Focus on Mission
Contains: anonymization, feature extraction, scoring, template questions,
logging, bias audit, contrast checking, PDF generation.

Public-sector responsible AI guardrails are applied throughout.
"""

import re
import hashlib
import datetime
import io
import json
import logging
from collections import Counter
from typing import Dict, List, Tuple, Any, Optional

# Configure logging for contrast warnings and audit trail
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =============================================================================
# PII ANONYMIZATION
# =============================================================================
# Regex patterns for common PII. Extend as needed for your use case.

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(\+?\d[\d\-\s\(\)]{7,}\d)")
SSN_RE = re.compile(r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b")
ADDR_RE = re.compile(r"\d{1,5}\s+\w+\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct)\b", re.IGNORECASE)
NAME_RE = re.compile(r"(Name:\s*)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)")
DATE_RE = re.compile(r"\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b")


def anonymize_text(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Anonymize PII in text. Returns (anonymized_text, mapping).

    The mapping is kept in-memory only and should NOT be persisted.
    This is critical for public-sector responsible AI compliance.
    """
    t = text
    mapping = {}

    # SSNs (high priority - must redact)
    for m in SSN_RE.findall(t):
        placeholder = "[SSN_REDACTED]"
        mapping[placeholder] = mapping.get(placeholder, [])
        if isinstance(mapping[placeholder], list):
            mapping[placeholder] = m
        t = t.replace(m, placeholder)

    # Emails
    for m in EMAIL_RE.findall(t):
        placeholder = "[EMAIL_REDACTED]"
        mapping[placeholder] = m
        t = t.replace(m, placeholder)

    # Phones
    for m in PHONE_RE.findall(t):
        placeholder = "[PHONE_REDACTED]"
        mapping[placeholder] = m
        t = t.replace(m, placeholder)

    # Addresses
    for m in ADDR_RE.findall(t):
        placeholder = "[ADDR_REDACTED]"
        t = t.replace(m, placeholder)

    # Names (best effort - pattern-based)
    t = NAME_RE.sub(r"\1[NAME_REDACTED]", t)

    # Dates of birth patterns (optional, be careful not to remove job dates)
    # Keeping this commented as it may over-redact
    # t = DATE_RE.sub("[DATE_REDACTED]", t)

    return t, mapping


# =============================================================================
# FEATURE EXTRACTION
# =============================================================================

SKILL_KEYWORDS = [
    # Technical Skills
    "python", "sql", "tableau", "power bi", "qlik", "azure", "pandas", "numpy",
    "r", "arcgis", "project management", "agile", "scrum", "docker",
    "kubernetes", "java", "javascript", "aws", "gcp", "excel", "sas",
    "spss", "matplotlib", "scikit-learn", "machine learning", "data visualization",
    "etl", "data warehouse", "snowflake", "databricks", "spark", "hadoop",

    # Government/Public Sector Skills
    "procurement", "contracting", "contract administration", "compliance",
    "government regulations", "policy development", "stakeholder engagement",
    "budget management", "financial reporting", "cost analysis",
    "data analysis", "business analysis", "technical analysis",
    "report writing", "dashboard development",

    # Regulatory & Compliance
    "foia", "public records", "ada compliance", "508 compliance",
    "eeo", "equal opportunity", "procurement regulations",
    "federal regulations", "state regulations",

    # Soft Skills (Government Context)
    "stakeholder management", "governmental officials", "public sector",
    "cross-functional collaboration", "technical documentation",
    "requirements gathering", "process improvement"
]

CERTIFICATION_KEYWORDS = [
    "pmp", "cissp", "aws certified", "azure certified", "tableau certified",
    "google certified", "comptia", "itil", "six sigma", "scrum master",
    "certified public manager", "cpm", "government finance", "cgfm",
    "certified government auditing professional", "cgap"
]


def extract_features(text: str) -> Dict[str, Any]:
    """
    Extract candidate features from resume text.
    Returns dict with skills, years_experience, education, certifications, evidence_lines.
    """
    text_l = text.lower()

    # Skills detection
    skills = [k for k in SKILL_KEYWORDS if k in text_l]

    # Certifications detection
    certs = [c for c in CERTIFICATION_KEYWORDS if c in text_l]

    # Years of experience: find patterns like 'X years' or 'X+ years'
    yrs = 0
    year_patterns = [
        r"(\d{1,2})\+?\s*years?\s*(?:of\s*)?experience",
        r"(\d{1,2})\+?\s*years?\s*(?:in|with|of)",
        r"experience[:\s]+(\d{1,2})\+?\s*years?"
    ]
    for pattern in year_patterns:
        m = re.search(pattern, text_l)
        if m:
            yrs = max(yrs, int(m.group(1)))

    # Education heuristic
    edu = "Other"
    edu_level = 0
    if "ph.d" in text_l or "phd" in text_l or "doctorate" in text_l:
        edu = "Ph.D."
        edu_level = 3
    elif "m.s." in text_l or "master" in text_l or "m.a." in text_l or "mba" in text_l:
        edu = "M.S."
        edu_level = 2
    elif "b.s." in text_l or "bachelor" in text_l or "b.a." in text_l:
        edu = "B.S."
        edu_level = 1

    # Evidence lines: capture context around skill mentions
    evidence = {}
    for s in skills[:5]:  # Limit to top 5 to avoid excessive evidence
        idx = text_l.find(s)
        if idx >= 0:
            start = max(0, idx - 60)
            end = min(len(text), idx + len(s) + 100)
            snippet = text[start:end].strip().replace("\n", " ")
            evidence[s] = snippet

    return {
        "skills": skills,
        "certifications": certs,
        "years_experience": yrs,
        "education": edu,
        "education_level": edu_level,
        "evidence_lines": evidence
    }


# =============================================================================
# SCORING
# =============================================================================

def score_candidate(features: Dict[str, Any], weights: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
    """
    Score a candidate based on extracted features and configurable weights.
    Returns (total_score, breakdown_dict).
    """
    score = 0.0
    breakdown = {}

    # Skills score
    num_skills = len(features.get("skills", []))
    score_skills = weights.get("skills", 1.0) * min(num_skills, 10)  # Cap at 10 skills
    breakdown["skills"] = round(score_skills, 2)
    score += score_skills

    # Experience score
    yrs = features.get("years_experience", 0)
    score_exp = weights.get("experience", 1.0) * min(yrs, 15)  # Cap at 15 years
    breakdown["experience"] = round(score_exp, 2)
    score += score_exp

    # Education score
    edu_level = features.get("education_level", 0)
    score_edu = weights.get("education", 0.0) * edu_level
    breakdown["education"] = round(score_edu, 2)
    score += score_edu

    # Certifications score
    num_certs = len(features.get("certifications", []))
    score_certs = weights.get("certifications", 0.0) * min(num_certs, 5)
    breakdown["certifications"] = round(score_certs, 2)
    score += score_certs

    return round(score, 2), breakdown


# =============================================================================
# LEVEL MATCHING & QUALIFICATION GATING
# =============================================================================

def detect_qualification_level(years_experience: int, level_thresholds: List[int]) -> int:
    """
    Determine which job level a candidate qualifies for based on experience.

    Args:
        years_experience: Years of relevant experience
        level_thresholds: List of minimum years required for each level (e.g., [0, 1, 2, 3, 4] for I-V)

    Returns:
        Index of highest qualifying level (0-based)

    Example:
        detect_qualification_level(2, [0, 1, 2, 3, 4]) -> 2 (qualifies for level III)
    """
    qualified_level = 0
    for i, threshold in enumerate(level_thresholds):
        if years_experience >= threshold:
            qualified_level = i
        else:
            break
    return qualified_level


def check_education_requirement(features: Dict, requirement: str = "Bachelor's") -> Tuple[bool, str]:
    """
    Check if candidate meets education requirement, including substitution rules.

    Public sector often allows: "Relevant work experience may be substituted for degree on a year per year basis"
    For Bachelor's: 4 years experience can substitute

    Args:
        features: Candidate features dict with 'education', 'education_level', 'years_experience'
        requirement: Education requirement string

    Returns:
        (meets_requirement: bool, explanation: str)
    """
    edu = features.get("education", "Other")
    edu_level = features.get("education_level", 0)
    years_exp = features.get("years_experience", 0)

    # Direct match
    if requirement == "Bachelor's" or requirement == "Bachelor's or equivalent experience":
        if edu_level >= 1:  # Has Bachelor's, Master's, or Ph.D.
            return True, f"Has {edu}"
        elif years_exp >= 4:
            return True, f"Meets requirement via work experience substitution ({years_exp} years)"
        else:
            return False, f"Needs Bachelor's OR 4+ years experience (has {years_exp} years)"

    elif requirement == "Master's":
        if edu_level >= 2:
            return True, f"Has {edu}"
        elif years_exp >= 6:  # Master's typically = 6 years (4 + 2)
            return True, f"Meets requirement via work experience substitution ({years_exp} years)"
        else:
            return False, f"Needs Master's OR 6+ years experience (has {years_exp} years)"

    else:  # No specific requirement or "Other"
        return True, "No specific education requirement"


def check_mandatory_skills(candidate_skills: List[str], required_skills: List[str]) -> Tuple[bool, List[str]]:
    """
    Check if candidate has all mandatory skills.

    Args:
        candidate_skills: List of skills detected in resume
        required_skills: List of required skills for the job

    Returns:
        (has_all_required: bool, missing_skills: List[str])
    """
    candidate_skills_lower = [s.lower() for s in candidate_skills]
    missing = []

    for req_skill in required_skills:
        # Check for any match (handles variations like "Tableau" vs "tableau certified")
        if not any(req_skill.lower() in cs for cs in candidate_skills_lower):
            missing.append(req_skill)

    return len(missing) == 0, missing


def gate_candidate(features: Dict, job_info: Dict) -> Tuple[bool, Dict[str, Any]]:
    """
    Apply mandatory qualification gates before scoring.

    Args:
        features: Candidate features
        job_info: Job information with requirements (from JOB_LIBRARY)

    Returns:
        (is_qualified: bool, gate_results: Dict)
    """
    gate_results = {
        "education_check": {"passed": True, "message": ""},
        "skills_check": {"passed": True, "message": ""},
        "level_qualified": 0,
        "level_name": ""
    }

    # Check education requirement
    if "required_education" in job_info:
        edu_passed, edu_msg = check_education_requirement(features, job_info["required_education"])
        gate_results["education_check"] = {"passed": edu_passed, "message": edu_msg}

    # Check mandatory skills (must have ALL of these)
    if "required_skills" in job_info:
        skills_passed, missing = check_mandatory_skills(
            features.get("skills", []),
            job_info["required_skills"]
        )
        gate_results["skills_check"] = {
            "passed": skills_passed,
            "message": f"Missing required skills: {', '.join(missing)}" if missing else "All required skills present"
        }

    # Check "any of" skills (must have AT LEAST ONE)
    if "required_any_of" in job_info:
        candidate_skills_lower = [s.lower() for s in features.get("skills", [])]
        required_any = job_info["required_any_of"]

        # Check if candidate has at least one of the required tools
        has_any = any(
            any(req.lower() in cs for cs in candidate_skills_lower)
            for req in required_any
        )

        if not has_any:
            gate_results["skills_check"] = {
                "passed": False,
                "message": f"Missing required tools: Must have at least one of: {', '.join(required_any)}"
            }

    # Determine qualification level
    if "levels" in job_info and "experience_required" in job_info:
        level_idx = detect_qualification_level(
            features.get("years_experience", 0),
            job_info["experience_required"]
        )
        gate_results["level_qualified"] = level_idx
        gate_results["level_name"] = job_info["levels"][level_idx] if level_idx < len(job_info["levels"]) else "Unknown"

    # Overall qualification = pass all gates
    is_qualified = (
        gate_results["education_check"]["passed"] and
        gate_results["skills_check"]["passed"]
    )

    return is_qualified, gate_results


def score_candidates(candidates: List[Dict], weights: Dict[str, float]) -> List[Dict]:
    """
    Score and rank all candidates. Returns sorted list (highest score first).
    """
    out = []
    for c in candidates:
        f = c.get("features", {})
        s, b = score_candidate(f, weights)
        out.append({
            "anon_id": c.get("anon_id"),
            "score": s,
            "breakdown": b,
            "features": f,
            "filename": c.get("filename", ""),
            # Preserve qualification gating results
            "is_qualified": c.get("is_qualified", True),
            "gate_results": c.get("gate_results", {})
        })
    out = sorted(out, key=lambda x: x["score"], reverse=True)

    # Add rank
    for i, c in enumerate(out):
        c["rank"] = i + 1

    return out


# =============================================================================
# INTERVIEW QUESTIONS
# =============================================================================

def generate_template_questions(features: Dict[str, Any], job_text: str, gate_results: Dict = None) -> List[str]:
    """
    Generate template interview questions based on candidate features and qualification level.
    These are static, deterministic questions - no LLM involved.

    Enhanced for government/public sector positions with level-aware questioning.
    """
    qs = []
    skills = features.get("skills", [])
    years = features.get("years_experience", 0)
    edu = features.get("education", "Other")
    certs = features.get("certifications", [])
    level_name = gate_results.get("level_name", "") if gate_results else ""

    top_skills = skills[:3] if skills else ["relevant technical skills"]
    job_lower = job_text.lower()

    # Level-specific intro question
    if level_name and years > 0:
        qs.append(f"This position is at Level {level_name}. With {years} years of experience, describe a project that demonstrates your readiness for this level of responsibility.")
    elif years > 0:
        qs.append(f"With {years} years of experience, describe a significant challenge you overcame and what you learned.")
    else:
        qs.append("Tell us about a challenging project you've worked on and how you approached solving the problem.")

    # Skill-based questions
    if skills:
        qs.append(f"Describe a specific project where you applied {top_skills[0]}. What was your role, and what was the outcome?")
        if len(top_skills) > 1:
            qs.append(f"How have you used {' and '.join(top_skills[:2])} together to solve a business problem?")

    # Government/Public Sector specific questions
    if any(keyword in job_lower for keyword in ["government", "public sector", "state", "federal", "agency", "department"]):
        qs.append("Describe your experience working with government stakeholders, regulatory requirements, or public sector constraints.")
        qs.append("How do you balance efficiency with compliance and transparency in government work?")

    # Role-specific questions
    if "data" in job_lower and "analy" in job_lower:
        qs.append("Walk us through how you've translated complex data analysis into actionable insights for decision-makers.")
        if "dashboard" in job_lower or "visualization" in job_lower:
            qs.append("Describe your process for designing a dashboard that serves both technical and non-technical audiences.")

    if "business analy" in job_lower:
        qs.append("Describe a time when you had to gather requirements from multiple stakeholders with conflicting priorities. How did you resolve it?")
        if "process improvement" in job_lower or "process" in job_lower:
            qs.append("Tell us about a business process you improved. What was your methodology and what were the results?")

    if "contract" in job_lower or "procurement" in job_lower:
        qs.append("Describe your experience reviewing contracts for compliance with regulations and policies.")
        qs.append("How do you handle situations where contract requirements conflict with operational needs?")

    # Communication questions (critical for government roles)
    qs.append("Describe a time when you had to explain technical information to a non-technical audience, such as elected officials or senior management.")

    # Situational/behavioral questions
    if years >= 3:  # Mid to senior level
        qs.append("Tell us about a time you had to make a decision without complete information. How did you proceed?")
    else:  # Entry to junior level
        qs.append("How do you prioritize tasks when working on multiple projects with competing deadlines?")

    # Teamwork question (always relevant)
    qs.append("Describe a situation where you had to collaborate with colleagues from different departments or backgrounds to achieve a goal.")

    return qs[:8]  # Limit to 8 questions


# =============================================================================
# LOGGING (In-Memory Only)
# =============================================================================

_LOGS: List[Dict[str, Any]] = []


def log_record(record: Dict[str, Any]) -> None:
    """
    Log a record to in-memory storage.
    Records include timestamp and are NOT persisted to disk.
    """
    rec = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "type": "audit",
        **record
    }
    _LOGS.append(rec)
    logger.info(f"Logged record: {rec.get('anon_id', 'unknown')}")


def clear_logs() -> None:
    """Clear all in-memory logs. Called when user purges data."""
    global _LOGS
    _LOGS = []
    logger.info("All in-memory logs cleared.")


def get_logs() -> List[Dict[str, Any]]:
    """Return copy of current logs."""
    return _LOGS.copy()


def get_logs_csv(scored_list: List[Dict], display_name_mapping: Dict[str, str] = None) -> str:
    """
    Generate CSV string from scored candidates list.
    Does NOT include PII - only anonymized IDs and scores.

    Args:
        scored_list: List of scored candidate dicts
        display_name_mapping: Optional mapping of anon_id to display names (e.g., "Candidate A")
    """
    if display_name_mapping is None:
        display_name_mapping = {}

    headers = ["rank", "display_name", "anon_id", "score", "skills_score", "experience_score", "education_score", "certifications_score"]
    lines = [",".join(headers)]

    for s in scored_list:
        b = s.get("breakdown", {})
        display_name = display_name_mapping.get(s.get("anon_id", ""), "Unknown")
        row = [
            str(s.get("rank", "")),
            display_name,
            s.get("anon_id", ""),
            str(s.get("score", 0)),
            str(b.get("skills", 0)),
            str(b.get("experience", 0)),
            str(b.get("education", 0)),
            str(b.get("certifications", 0))
        ]
        lines.append(",".join(row))

    return "\n".join(lines)


# =============================================================================
# BIAS AUDIT STUB
# =============================================================================

def bias_audit_stub(scored_list: List[Dict]) -> Dict[str, Any]:
    """
    Placeholder bias audit function.

    In production, this would:
    - Analyze score distributions across demographic groups (if available)
    - Calculate disparate impact ratios
    - Flag potential adverse impact
    - Generate compliance documentation

    For this demo, we provide statistical summaries only.
    No demographic data is collected or analyzed.
    """
    if not scored_list:
        return {"error": "No candidates to audit", "candidates": 0}

    scores = [s["score"] for s in scored_list]

    # Basic statistics
    stats = {
        "candidates_evaluated": len(scores),
        "score_min": round(min(scores), 2),
        "score_max": round(max(scores), 2),
        "score_mean": round(sum(scores) / len(scores), 2),
        "score_median": round(sorted(scores)[len(scores) // 2], 2),
    }

    # Score distribution buckets
    buckets = {"low (0-10)": 0, "medium (10-25)": 0, "high (25+)": 0}
    for s in scores:
        if s < 10:
            buckets["low (0-10)"] += 1
        elif s < 25:
            buckets["medium (10-25)"] += 1
        else:
            buckets["high (25+)"] += 1

    # Top features by frequency
    feature_counts = Counter()
    for s in scored_list:
        for skill in s.get("features", {}).get("skills", []):
            feature_counts[skill] += 1

    return {
        "audit_timestamp": datetime.datetime.utcnow().isoformat(),
        "statistics": stats,
        "score_distribution": buckets,
        "top_skills_detected": feature_counts.most_common(10),
        "disparate_impact_note": "No demographic data available. In production, collect voluntary self-identification data to enable disparate impact analysis per EEOC guidelines.",
        "recommendation": "Human review required for all final hiring decisions. This tool provides decision support only."
    }


# =============================================================================
# CONTRAST RATIO CHECK (Accessibility)
# =============================================================================

def get_relative_luminance(hex_color: str) -> float:
    """
    Calculate relative luminance of a color per WCAG 2.1.
    Input: hex color string (e.g., "#E31937" or "E31937")
    """
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def check_contrast_ratio(fg_color: str, bg_color: str, context: str = "") -> float:
    """
    Check contrast ratio between foreground and background colors.
    Logs warning if ratio < 4.5:1 (WCAG AA for normal text).

    Returns the contrast ratio.
    """
    l1 = get_relative_luminance(fg_color)
    l2 = get_relative_luminance(bg_color)

    lighter = max(l1, l2)
    darker = min(l1, l2)

    ratio = (lighter + 0.05) / (darker + 0.05)

    if ratio < 4.5:
        logger.warning(
            f"CONTRAST WARNING{' (' + context + ')' if context else ''}: "
            f"Ratio {ratio:.2f}:1 between {fg_color} and {bg_color} "
            f"is below WCAG AA threshold of 4.5:1"
        )
    else:
        logger.info(f"Contrast check passed: {ratio:.2f}:1 {context}")

    return round(ratio, 2)


# =============================================================================
# PDF GENERATION
# =============================================================================

def generate_decision_pdf(candidate: Dict, job_summary: str = "", display_name: str = None) -> bytes:
    """
    Generate a PDF decision summary for a candidate.
    Uses reportlab for PDF generation.

    Args:
        candidate: Candidate dict with score, features, etc.
        job_summary: Optional job description text
        display_name: Optional display name like "Candidate A"

    Returns PDF as bytes.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
    except ImportError:
        logger.error("reportlab not installed. Returning empty PDF.")
        return b""

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.HexColor("#E31937")
    )

    story = []

    # Title
    story.append(Paragraph("Candidate Evaluation Summary", title_style))
    story.append(Paragraph("<i>DEMO ONLY - Not for real hiring decisions</i>", styles['Italic']))
    story.append(Spacer(1, 0.25*inch))

    # Candidate info
    display = display_name if display_name else candidate.get('anon_id', 'N/A')
    story.append(Paragraph(f"<b>Candidate:</b> {display}", styles['Normal']))
    story.append(Paragraph(f"<b>Technical ID:</b> {candidate.get('anon_id', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>Rank:</b> #{candidate.get('rank', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>Overall Score:</b> {candidate.get('score', 0)}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Score breakdown table
    breakdown = candidate.get("breakdown", {})
    table_data = [["Category", "Score"]]
    for cat, score in breakdown.items():
        table_data.append([cat.title(), str(score)])

    table = Table(table_data, colWidths=[2.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E31937")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F3F6F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.2*inch))

    # Skills detected
    features = candidate.get("features", {})
    skills = features.get("skills", [])
    if skills:
        story.append(Paragraph("<b>Skills Detected:</b>", styles['Normal']))
        story.append(Paragraph(", ".join(skills), styles['Normal']))
        story.append(Spacer(1, 0.1*inch))

    # Education
    story.append(Paragraph(f"<b>Education:</b> {features.get('education', 'Not detected')}", styles['Normal']))
    story.append(Paragraph(f"<b>Experience:</b> {features.get('years_experience', 0)} years", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Disclaimer
    story.append(Paragraph(
        "<b>Disclaimer:</b> This evaluation was generated by an AI-assisted tool for demonstration purposes. "
        "All candidate data has been anonymized. Final hiring decisions must be made by qualified human reviewers "
        "in compliance with applicable employment laws and organizational policies.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"<i>Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</i>", styles['Italic']))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
