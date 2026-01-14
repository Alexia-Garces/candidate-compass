"""
test_utils.py — Unit tests for Candidate Ranker utilities
==========================================================
Run with: pytest tests/test_utils.py -v
"""

import pytest
from utils import (
    anonymize_text,
    extract_features,
    score_candidate,
    score_candidates,
    generate_template_questions,
    get_relative_luminance,
    check_contrast_ratio,
    get_logs_csv,
    bias_audit_stub,
)


# =============================================================================
# ANONYMIZATION TESTS
# =============================================================================

class TestAnonymization:
    """Tests for PII anonymization functionality."""

    def test_anonymize_removes_email(self):
        """Email addresses should be redacted."""
        text = "Contact: john.doe@example.com for more info"
        anon, mapping = anonymize_text(text)
        assert "@" not in anon
        assert "[EMAIL_REDACTED]" in anon

    def test_anonymize_removes_phone(self):
        """Phone numbers should be redacted."""
        text = "Call me at 555-123-4567 or +1 (800) 555-1234"
        anon, mapping = anonymize_text(text)
        assert "555-123-4567" not in anon
        assert "[PHONE_REDACTED]" in anon

    def test_anonymize_removes_ssn(self):
        """Social Security Numbers should be redacted."""
        text = "SSN: 123-45-6789"
        anon, mapping = anonymize_text(text)
        assert "123-45-6789" not in anon
        assert "[SSN_REDACTED]" in anon

    def test_anonymize_removes_address(self):
        """Street addresses should be redacted."""
        text = "Located at 123 Main Street, Anytown"
        anon, mapping = anonymize_text(text)
        assert "123 Main Street" not in anon

    def test_anonymize_removes_name_label(self):
        """Names with 'Name:' prefix should be redacted."""
        text = "Name: John Smith\nExperience: 5 years"
        anon, mapping = anonymize_text(text)
        assert "John Smith" not in anon
        assert "[NAME_REDACTED]" in anon

    def test_anonymize_preserves_content(self):
        """Non-PII content should be preserved."""
        text = "5 years of Python experience with SQL and Tableau skills."
        anon, mapping = anonymize_text(text)
        assert "Python" in anon
        assert "SQL" in anon
        assert "5 years" in anon


# =============================================================================
# FEATURE EXTRACTION TESTS
# =============================================================================

class TestFeatureExtraction:
    """Tests for resume feature extraction."""

    def test_extract_skills(self):
        """Skills should be detected from text."""
        text = "Experienced with Python, SQL, and Tableau for data analysis."
        features = extract_features(text)
        assert "python" in features["skills"]
        assert "sql" in features["skills"]
        assert "tableau" in features["skills"]

    def test_extract_years_experience(self):
        """Years of experience should be extracted."""
        text = "5 years of experience in data analytics."
        features = extract_features(text)
        assert features["years_experience"] == 5

    def test_extract_years_experience_plus(self):
        """Years with + notation should be extracted."""
        text = "10+ years experience with Python"
        features = extract_features(text)
        assert features["years_experience"] == 10

    def test_extract_education_masters(self):
        """Master's degree should be detected."""
        text = "M.S. in Computer Science from State University"
        features = extract_features(text)
        assert features["education"] == "M.S."
        assert features["education_level"] == 2

    def test_extract_education_bachelors(self):
        """Bachelor's degree should be detected."""
        text = "B.S. in Data Science"
        features = extract_features(text)
        assert features["education"] == "B.S."
        assert features["education_level"] == 1

    def test_extract_education_phd(self):
        """Ph.D. should be detected."""
        text = "Ph.D. in Statistics"
        features = extract_features(text)
        assert features["education"] == "Ph.D."
        assert features["education_level"] == 3

    def test_extract_evidence_lines(self):
        """Evidence snippets should be captured around skill mentions."""
        text = "Led a team using Python to build data pipelines for analytics."
        features = extract_features(text)
        assert "python" in features["evidence_lines"]
        assert "pipeline" in features["evidence_lines"]["python"].lower()

    def test_extract_certifications(self):
        """Certifications should be detected."""
        text = "Certified PMP and AWS Certified Solutions Architect"
        features = extract_features(text)
        assert "pmp" in features["certifications"]
        assert "aws certified" in features["certifications"]


# =============================================================================
# SCORING TESTS
# =============================================================================

class TestScoring:
    """Tests for candidate scoring functionality."""

    def test_score_basic(self):
        """Basic scoring should work with default weights."""
        features = {
            "skills": ["python", "sql"],
            "years_experience": 5,
            "education": "B.S.",
            "education_level": 1,
            "certifications": [],
            "evidence_lines": {}
        }
        weights = {"skills": 1.0, "experience": 1.0, "education": 1.0, "certifications": 0.0}
        score, breakdown = score_candidate(features, weights)

        assert score > 0
        assert breakdown["skills"] == 2.0  # 2 skills * 1.0
        assert breakdown["experience"] == 5.0  # 5 years * 1.0
        assert breakdown["education"] == 1.0  # B.S. level 1 * 1.0

    def test_score_changes_with_weights(self):
        """Scores should change when weights are adjusted."""
        features = {
            "skills": ["python", "sql"],
            "years_experience": 5,
            "education": "B.S.",
            "education_level": 1,
            "certifications": [],
            "evidence_lines": {}
        }

        weights1 = {"skills": 1.0, "experience": 1.0, "education": 1.0, "certifications": 0.0}
        weights2 = {"skills": 3.0, "experience": 1.0, "education": 1.0, "certifications": 0.0}

        score1, _ = score_candidate(features, weights1)
        score2, _ = score_candidate(features, weights2)

        assert score2 > score1

    def test_score_caps_experience(self):
        """Experience scoring should cap at 15 years."""
        features = {
            "skills": [],
            "years_experience": 25,
            "education": "Other",
            "education_level": 0,
            "certifications": [],
            "evidence_lines": {}
        }
        weights = {"skills": 0.0, "experience": 1.0, "education": 0.0, "certifications": 0.0}
        score, breakdown = score_candidate(features, weights)

        assert breakdown["experience"] == 15.0  # Capped at 15

    def test_score_candidates_ranking(self):
        """Candidates should be ranked by score descending."""
        candidates = [
            {"anon_id": "low", "features": {"skills": ["python"], "years_experience": 1, "education_level": 0, "certifications": []}},
            {"anon_id": "high", "features": {"skills": ["python", "sql", "tableau"], "years_experience": 10, "education_level": 2, "certifications": ["pmp"]}},
            {"anon_id": "mid", "features": {"skills": ["python", "sql"], "years_experience": 5, "education_level": 1, "certifications": []}},
        ]
        weights = {"skills": 1.0, "experience": 1.0, "education": 1.0, "certifications": 1.0}

        scored = score_candidates(candidates, weights)

        assert scored[0]["anon_id"] == "high"
        assert scored[1]["anon_id"] == "mid"
        assert scored[2]["anon_id"] == "low"
        assert scored[0]["rank"] == 1
        assert scored[2]["rank"] == 3


# =============================================================================
# INTERVIEW QUESTIONS TESTS
# =============================================================================

class TestInterviewQuestions:
    """Tests for interview question generation."""

    def test_template_questions_include_skills(self):
        """Template questions should reference detected skills."""
        features = {"skills": ["python", "sql"], "years_experience": 5, "education": "B.S."}
        job_text = "Data analyst role"

        questions = generate_template_questions(features, job_text)

        assert len(questions) > 0
        assert any("python" in q.lower() for q in questions)

    def test_template_questions_include_experience(self):
        """Template questions should reference years of experience."""
        features = {"skills": ["python"], "years_experience": 8, "education": "M.S."}
        job_text = "Senior role"

        questions = generate_template_questions(features, job_text)

        assert any("8" in q or "years" in q.lower() for q in questions)

    def test_template_questions_job_specific(self):
        """Questions should adapt to job description keywords."""
        features = {"skills": ["python"], "years_experience": 5, "education": "B.S."}
        job_text = "Build dashboards and work with stakeholders in government"

        questions = generate_template_questions(features, job_text)

        assert any("dashboard" in q.lower() or "stakeholder" in q.lower() or "government" in q.lower()
                   for q in questions)


# =============================================================================
# CONTRAST RATIO TESTS
# =============================================================================

class TestContrastRatio:
    """Tests for accessibility contrast checking."""

    def test_luminance_white(self):
        """White should have luminance of 1.0."""
        lum = get_relative_luminance("#FFFFFF")
        assert abs(lum - 1.0) < 0.01

    def test_luminance_black(self):
        """Black should have luminance of 0.0."""
        lum = get_relative_luminance("#000000")
        assert abs(lum - 0.0) < 0.01

    def test_contrast_black_white(self):
        """Black on white should have maximum contrast (21:1)."""
        ratio = check_contrast_ratio("#000000", "#FFFFFF", "test")
        assert ratio == 21.0

    def test_contrast_warning_low(self):
        """Low contrast should be detected (test doesn't fail, just logs)."""
        # Light gray on white - poor contrast
        ratio = check_contrast_ratio("#CCCCCC", "#FFFFFF", "low contrast test")
        assert ratio < 4.5

    def test_contrast_cgi_red_white(self):
        """CGI Red (#E31937) on white should have good contrast."""
        ratio = check_contrast_ratio("#E31937", "#FFFFFF", "CGI red test")
        assert ratio > 4.0  # Should be around 4.5


# =============================================================================
# CSV EXPORT TESTS
# =============================================================================

class TestCSVExport:
    """Tests for CSV generation."""

    def test_csv_headers(self):
        """CSV should have correct headers."""
        scored = [{"anon_id": "abc123", "score": 10.5, "rank": 1, "breakdown": {"skills": 5.0, "experience": 3.0, "education": 2.0, "certifications": 0.5}}]
        csv = get_logs_csv(scored)

        lines = csv.split("\n")
        assert "rank" in lines[0]
        assert "anon_id" in lines[0]
        assert "score" in lines[0]

    def test_csv_data_rows(self):
        """CSV should include candidate data."""
        scored = [
            {"anon_id": "abc123", "score": 10.5, "rank": 1, "breakdown": {"skills": 5.0, "experience": 3.0, "education": 2.0, "certifications": 0.5}},
            {"anon_id": "def456", "score": 8.0, "rank": 2, "breakdown": {"skills": 4.0, "experience": 2.0, "education": 1.0, "certifications": 1.0}},
        ]
        csv = get_logs_csv(scored)

        assert "abc123" in csv
        assert "def456" in csv
        assert "10.5" in csv


# =============================================================================
# BIAS AUDIT TESTS
# =============================================================================

class TestBiasAudit:
    """Tests for bias audit functionality."""

    def test_audit_returns_statistics(self):
        """Audit should return score statistics."""
        scored = [
            {"anon_id": "a", "score": 10.0, "features": {"skills": ["python"]}},
            {"anon_id": "b", "score": 20.0, "features": {"skills": ["sql"]}},
            {"anon_id": "c", "score": 30.0, "features": {"skills": ["python", "sql"]}},
        ]

        report = bias_audit_stub(scored)

        assert "statistics" in report
        assert report["statistics"]["candidates_evaluated"] == 3
        assert report["statistics"]["score_min"] == 10.0
        assert report["statistics"]["score_max"] == 30.0

    def test_audit_empty_list(self):
        """Audit should handle empty candidate list."""
        report = bias_audit_stub([])

        assert "error" in report

    def test_audit_includes_disclaimer(self):
        """Audit should include responsible AI disclaimer."""
        scored = [{"anon_id": "a", "score": 10.0, "features": {"skills": []}}]

        report = bias_audit_stub(scored)

        assert "recommendation" in report
        assert "human" in report["recommendation"].lower()
