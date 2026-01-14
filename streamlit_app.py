"""
streamlit_app.py — CandidateCompass
====================================
Navigate Talent, Focus on Mission
AI-assisted, human-reviewed resume screening optimized for public sector workshops.
Responsible AI guardrails applied throughout.

Developer Notes:
- BRANDING dict at top controls colors, logo, gradients
- Gradient file auto-detected; falls back to CSS gradient
- All CSS injection is minimal and documented as fragile (unsafe_allow_html)
"""

import streamlit as st
import hashlib
import os
import json
import base64
from pathlib import Path

from utils import (
    anonymize_text,
    extract_features,
    score_candidates,
    generate_template_questions,
    log_record,
    clear_logs,
    get_logs_csv,
    bias_audit_stub,
    check_contrast_ratio,
    generate_decision_pdf,
)

# =============================================================================
# BRANDING CONFIGURATION
# =============================================================================
# Modify these values to customize the app's appearance.
# See assets/brand_guide.md for full documentation.

BRANDING = {
    "primaryColor": "#E31937",          # CGI Red (R227 G25 B55)
    "purpleColor": "#5236ab",           # CGI Purple (R82 G54 B171)
    "gradientA": "#E31937",             # Gradient A (Red to Orange)
    "gradientB": "#FF6B00",             # Gradient B (Orange)
    "textColor": "#333333",              # Main text color (R51 G51 B51)
    "backgroundColor": "#FFFFFF",        # Main background
    "secondaryBackgroundColor": "#F3F6F9",  # Sidebar, cards
    "logo_path": "assets/CGI_logo_rgb_white.png",  # White logo for gradient bg
    "logo_path_dark": "assets/CGI_logo_color_rgb.png",  # Color logo fallback
    "logo_alt": "CGI logo",
    "use_gradient": True,
    "gradient_file": "assets/gradients/header-gradient.svg",
    "gradient_css_fallback": "linear-gradient(90deg, #E31937 0%, #FF6B00 100%)",
}

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="CandidateCompass",
    page_icon="assets/favicon.ico" if os.path.exists("assets/favicon.ico") else "🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_candidate_display_name(index: int) -> str:
    """
    Generate display name for candidate (A, B, C, etc).

    Args:
        index: Zero-based index of candidate

    Returns:
        Display name like "Candidate A", "Candidate B", etc.
    """
    if index < 26:
        letter = chr(65 + index)  # A-Z
    else:
        letter = f"A{index - 25}"  # A1, A2, A3... for 27+
    return f"Candidate {letter}"


def get_candidate_display_name(anon_id: str) -> str:
    """
    Get display name for candidate from session state mapping.
    Falls back to anon_id if mapping not found.

    Args:
        anon_id: Technical anonymous ID

    Returns:
        Display name like "Candidate A" or anon_id if not mapped
    """
    mapping = st.session_state.get("candidate_display_names", {})
    return mapping.get(anon_id, f"`{anon_id}`")


def get_base64_image(image_path: str) -> str:
    """Convert image to base64 for embedding in HTML."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def detect_gradient_file() -> tuple:
    """
    Detect available gradient file. Returns (file_path, is_svg).
    Checks for SVG first, then PNG, then falls back to None.
    """
    gradient_dir = Path("assets/gradients")

    # Priority order: configured file, then SVG, then PNG
    if os.path.exists(BRANDING["gradient_file"]):
        return BRANDING["gradient_file"], BRANDING["gradient_file"].endswith(".svg")

    for ext in [".svg", ".png", ".jpg"]:
        for f in gradient_dir.glob(f"*header*{ext}"):
            return str(f), ext == ".svg"

    return None, False


def get_logo_path() -> str:
    """Get the appropriate logo path, with fallbacks."""
    # For gradient background, prefer white logo
    if os.path.exists(BRANDING["logo_path"]):
        return BRANDING["logo_path"]
    if os.path.exists(BRANDING["logo_path_dark"]):
        return BRANDING["logo_path_dark"]
    if os.path.exists("assets/logo.png"):
        return "assets/logo.png"
    return ""


# =============================================================================
# HEADER / HERO WITH GRADIENT
# =============================================================================
# WARNING: This section uses unsafe_allow_html=True for custom styling.
# This is fragile and may break with Streamlit updates.
# Keep CSS minimal and test thoroughly after Streamlit upgrades.

def render_header():
    """
    Render the hero header with logo and title using native Streamlit components.
    Simpler approach that avoids HTML rendering issues.
    """
    logo_path = get_logo_path()

    # Use columns for logo + title layout
    col1, col2 = st.columns([1, 4])

    with col1:
        if logo_path and os.path.exists(logo_path):
            st.image(logo_path, width=180)
        else:
            st.markdown(f"""
                <div style="background:{BRANDING["primaryColor"]}; color:white; padding:12px 20px;
                            border-radius:4px; font-weight:bold; font-size:1.3rem; text-align:center;">
                    CGI
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.title("CandidateCompass")
        st.caption("Navigate Talent, Focus on Mission")
        st.caption("AI-assisted, human-reviewed resume screening")

    # Secure demo experience banner
    st.markdown(
        f"""
        <div style="background-color: {BRANDING['secondaryBackgroundColor']};
                    border-left: 4px solid {BRANDING['purpleColor']};
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">🔒</span>
                <strong>Secure Demo Experience</strong>
            </div>
            <p style="margin: 0.5rem 0 0 2rem; color: #666;">
                This tool uses anonymized, fictional candidate data for demonstration purposes only.
                No personally identifiable information (PII) is processed. Results are for
                training and exploration, not employment decisions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()


# Render the header
render_header()

# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================

st.sidebar.header("Controls")

st.sidebar.markdown("**Data Management**")

# Purge logs button
if st.sidebar.button("Purge All Data", type="secondary"):
    clear_logs()
    st.session_state["candidates"] = []
    st.session_state["job_text"] = ""
    st.sidebar.success("All in-memory data purged.")

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

if "candidates" not in st.session_state:
    st.session_state["candidates"] = []
if "job_text" not in st.session_state:
    st.session_state["job_text"] = ""

# =============================================================================
# FILE UPLOAD SECTION
# =============================================================================

st.subheader("1. Select or Upload Job")

# Real government job selector (simplified to single demo job)
JOB_LIBRARY = {
    "Data Analyst I-V (Infrastructure)": {
        "file": "sample_data/generated/ActualJobs/TxDOT Data Analyst 1-5.pdf",
        "levels": ["I", "II", "III", "IV", "V"],
        "experience_required": [0, 1, 2, 3, 4],
        "required_skills": ["SQL"],  # Core required skills
        "required_any_of": ["Tableau", "Power BI", "Qlik"],  # Need at least ONE visualization tool
        "required_education": "Bachelor's or equivalent experience",
        "description": "Infrastructure Division - Data analysis and research position with 5 career levels"
    }
}

# Quick Start Guide
with st.expander("ℹ️ How to Use This Demo"):
    st.markdown("""
    **Quick Start Guide:**
    1. Click "Launch Demo" to load sample data
    2. Review AI-generated candidate rankings
    3. Explore how scoring weights affect results
    4. Adjust criteria to match your agency's needs

    *This interactive demo lets you experience AI-assisted resume screening in a safe, controlled environment.*
    """)

col1, col2 = st.columns([3, 2])

with col1:
    job_selector = st.selectbox(
        "Select a Real Government Job",
        options=list(JOB_LIBRARY.keys()) + ["Upload Custom Job"],
        index=0,  # Pre-select "Data Analyst I-V (Infrastructure)" by default
        help="Pre-loaded with Data Analyst position, or upload your own job description"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background-color: {BRANDING['secondaryBackgroundColor']};
                    border-left: 4px solid {BRANDING['purpleColor']};
                    padding: 0.75rem;
                    border-radius: 0.5rem;
                    margin: 0 0 1rem 0;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">ℹ️</span>
                <strong>Quick Start:</strong>
            </div>
            <p style="margin: 0.25rem 0 0 1.7rem; color: #666; font-size: 0.9rem;">
                Pre-loads a government job posting with 8 sample candidate resumes
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🚀 Launch Demo", type="primary", use_container_width=True):
        # Auto-select first job and load demo data
        selected_job_key = list(JOB_LIBRARY.keys())[0]
        job_info = JOB_LIBRARY[selected_job_key]

        # Load job description from PDF
        from pypdf import PdfReader
        job_path = Path(job_info["file"])
        if job_path.exists():
            reader = PdfReader(job_path)
            job_text = "\n".join([p.extract_text() or "" for p in reader.pages])

            # Anonymize job description
            from anonymize_jobs import anonymize_job_text
            st.session_state["job_text"] = anonymize_job_text(job_text)
            st.session_state["selected_job"] = selected_job_key
            st.session_state["job_info"] = job_info

            # Load demo resumes
            demo_dir = Path("sample_data/generated/DemoResumes")
            if demo_dir.exists():
                st.session_state["candidates"] = []
                st.session_state["candidate_display_names"] = {}  # Reset mapping
                pdf_files = sorted(demo_dir.glob("*.pdf"))
                for idx, f in enumerate(pdf_files):
                    anon_id = f"demo_{idx}_{f.stem[-8:]}"
                    st.session_state["candidates"].append({
                        "filename": str(f),
                        "text": "",
                        "anon_id": anon_id
                    })
                    # Create display name mapping
                    st.session_state["candidate_display_names"][anon_id] = generate_candidate_display_name(idx)
                st.success(f"✅ Demo loaded: {selected_job_key} + {len(pdf_files)} candidates")
            else:
                st.error("Demo resume data not found")
        else:
            st.error(f"Job file not found: {job_path}")

# Handle job selector changes
if job_selector != "Upload Custom Job" and job_selector in JOB_LIBRARY:
    job_info = JOB_LIBRARY[job_selector]

    # Display job info
    st.markdown(
        f"""
        <div style="background-color: {BRANDING['secondaryBackgroundColor']};
                    border-left: 4px solid {BRANDING['purpleColor']};
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin: 1rem 0;">
            <strong>{job_selector}</strong><br>
            <span style="color: #666;">{job_info['description']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load job description
    from pypdf import PdfReader
    job_path = Path(job_info["file"])
    if job_path.exists():
        reader = PdfReader(job_path)
        job_text = "\n".join([p.extract_text() or "" for p in reader.pages])

        # Anonymize job description
        from anonymize_jobs import anonymize_job_text
        st.session_state["job_text"] = anonymize_job_text(job_text)
        st.session_state["selected_job"] = job_selector
        st.session_state["job_info"] = job_info

        # Display detailed job requirements card
        st.markdown("---")
        st.markdown("#### 📋 Job Requirements Summary")

        col_req1, col_req2 = st.columns(2)

        with col_req1:
            st.markdown("**Required Skills (Must Have):**")
            req_skills = job_info.get("required_skills", [])
            if req_skills:
                for skill in req_skills:
                    st.markdown(f"- {skill}")
            else:
                st.markdown("- *Not specified*")

            st.markdown("")
            st.markdown("**Required Tools (At Least One):**")
            req_any = job_info.get("required_any_of", [])
            if req_any:
                for tool in req_any:
                    st.markdown(f"- {tool}")
            else:
                st.markdown("- *Not specified*")

        with col_req2:
            st.markdown("**Education Requirement:**")
            st.markdown(f"- {job_info.get('required_education', 'Not specified')}")
            st.caption("*Work experience may substitute for degree on a year-per-year basis*")

            st.markdown("")
            st.markdown("**Experience by Level:**")
            levels = job_info.get("levels", [])
            exp_required = job_info.get("experience_required", [])
            if levels and exp_required:
                for level, exp in zip(levels, exp_required):
                    st.markdown(f"- **Level {level}:** {exp}+ years")
            else:
                st.markdown("- *Not specified*")

        st.markdown("---")
    else:
        st.error(f"Job file not found: {job_path}")

# Show custom upload if selected
uploaded_jd = None
if job_selector == "Upload Custom Job":
    uploaded_jd = st.file_uploader(
        "Upload Job Description (PDF or TXT)",
        type=["pdf", "txt"],
        key="jd_upload",
        help="Upload your own job requirements document"
    )
    if uploaded_jd:
        st.session_state["job_text"] = extract_text_from_file(uploaded_jd)
        st.success(f"✅ Custom job loaded: {len(st.session_state['job_text'])} characters")

st.subheader("2. Upload Candidate Resumes")

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_resumes = st.file_uploader(
        "Resumes (PDF or TXT) — Multiple files allowed",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        key="resume_upload",
        help="Upload candidate resumes for evaluation"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Load Demo Resumes", use_container_width=True):
        demo_dir = Path("sample_data/generated/DemoResumes")
        if demo_dir.exists():
            # Load all demo resume PDFs
            st.session_state["candidates"] = []
            st.session_state["candidate_display_names"] = {}  # Reset mapping
            pdf_files = sorted(demo_dir.glob("*.pdf"))
            for idx, f in enumerate(pdf_files):
                anon_id = f"demo_{idx}_{f.stem[-8:]}"
                st.session_state["candidates"].append({
                    "filename": str(f),
                    "text": "",
                    "anon_id": anon_id
                })
                # Create display name mapping
                st.session_state["candidate_display_names"][anon_id] = generate_candidate_display_name(idx)
            st.success(f"Loaded {len(pdf_files)} demo resumes")
        else:
            st.error("Demo data not found. Check sample_data/generated/ExampleJob/")


def extract_text_from_file(file_obj) -> str:
    """Extract text from uploaded file (PDF or TXT)."""
    if file_obj.type == "application/pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_obj)
            pages = [p.extract_text() or "" for p in reader.pages]
            return "\n".join(pages)
        except Exception as e:
            st.warning(f"PDF extraction failed: {e}")
            return file_obj.getvalue().decode(errors="ignore")
    else:
        return file_obj.getvalue().decode(errors="ignore")


def process_uploads(jd_file, resume_files):
    """Process uploaded job description and resumes."""
    if jd_file is not None:
        st.session_state["job_text"] = extract_text_from_file(jd_file)

    if resume_files:
        cand_list = []
        for f in resume_files:
            text = extract_text_from_file(f)
            # Anonymize immediately
            anon_text, _ = anonymize_text(text)
            # Generate anonymous ID from content hash
            anon_id = hashlib.sha256(anon_text.encode()).hexdigest()[:12]
            cand_list.append({
                "filename": f.name,
                "text": anon_text,
                "anon_id": anon_id
            })
        st.session_state["candidates"] = cand_list


# Process resume uploads
if uploaded_resumes:
    cand_list = []
    st.session_state["candidate_display_names"] = {}  # Reset mapping
    for idx, f in enumerate(uploaded_resumes):
        text = extract_text_from_file(f)
        # Anonymize immediately
        anon_text, _ = anonymize_text(text)
        # Generate anonymous ID from content hash
        anon_id = hashlib.sha256(anon_text.encode()).hexdigest()[:12]
        cand_list.append({
            "filename": f.name,
            "text": anon_text,
            "anon_id": anon_id
        })
        # Create display name mapping
        st.session_state["candidate_display_names"][anon_id] = generate_candidate_display_name(idx)
    st.session_state["candidates"] = cand_list
    st.success(f"✅ Loaded {len(cand_list)} candidate resumes")

# Show current data status
if st.session_state.get("job_text"):
    st.success(f"✅ Job loaded: {st.session_state.get('selected_job', 'Custom Job')}")
if st.session_state.get("candidates"):
    st.success(f"✅ Candidates loaded: {len(st.session_state['candidates'])}")
elif not st.session_state.get("candidates"):
    st.warning("⚠️ No candidates loaded. Upload resumes or click 'Launch Demo'.")

st.divider()

# =============================================================================
# SCORING RUBRIC
# =============================================================================

st.subheader("3. Adjust Scoring Rubric (Optional)")

st.markdown("*Adjust weights to prioritize different qualifications:*")

col_w1, col_w2, col_w3, col_w4 = st.columns(4)

with col_w1:
    weight_skills = st.slider("Skills", 0.0, 5.0, 3.0, 0.5, help="Weight for matching skills")
with col_w2:
    weight_exp = st.slider("Experience", 0.0, 5.0, 2.0, 0.5, help="Weight for years of experience")
with col_w3:
    weight_edu = st.slider("Education", 0.0, 5.0, 1.0, 0.5, help="Weight for education level")
with col_w4:
    weight_certs = st.slider("Certifications", 0.0, 3.0, 0.5, 0.5, help="Weight for certifications")

weights = {
    "skills": weight_skills,
    "experience": weight_exp,
    "education": weight_edu,
    "certifications": weight_certs,
}

col_info, col_reset = st.columns([3, 1])

with col_info:
    st.caption("**How scoring works:** Each category contributes based on its weight. "
               "Skills capped at 10, experience at 15 years to prevent outliers. "
               "Adjust weights to reflect hiring priorities.")

with col_reset:
    if st.button("Reset to Defaults", use_container_width=True):
        st.rerun()

# =============================================================================
# FEATURE EXTRACTION AND SCORING
# =============================================================================

candidates = st.session_state.get("candidates", [])

# Extract text from demo PDFs if needed
for c in candidates:
    if not c.get("text"):
        try:
            p = Path(c["filename"])
            if p.exists() and p.suffix.lower() == ".pdf":
                from pypdf import PdfReader
                reader = PdfReader(str(p))
                raw_text = "\n".join([page.extract_text() or "" for page in reader.pages])
                anon_text, _ = anonymize_text(raw_text)
                c["text"] = anon_text
            elif p.exists():
                raw_text = p.read_text()
                anon_text, _ = anonymize_text(raw_text)
                c["text"] = anon_text
        except Exception as e:
            c["text"] = ""

    # Extract features
    if c.get("text") and not c.get("features"):
        c["features"] = extract_features(c["text"])

    # Apply qualification gating if job info available
    if c.get("features") and st.session_state.get("job_info"):
        from utils import gate_candidate
        is_qualified, gate_results = gate_candidate(c["features"], st.session_state["job_info"])
        c["is_qualified"] = is_qualified
        c["gate_results"] = gate_results
    else:
        # No gating if no job info (custom uploads)
        c["is_qualified"] = True
        c["gate_results"] = {}

# Score and rank candidates
scored = score_candidates(candidates, weights) if candidates else []

# Separate qualified and disqualified candidates
qualified_candidates = [c for c in scored if c.get("is_qualified", True)]
disqualified_candidates = [c for c in scored if not c.get("is_qualified", True)]

# =============================================================================
# RANKED RESULTS
# =============================================================================

st.subheader("3. Ranked Candidates")

if not scored:
    st.markdown(
        f"""
        <div style="background-color: {BRANDING['secondaryBackgroundColor']};
                    border-left: 4px solid {BRANDING['purpleColor']};
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">ℹ️</span>
                <span style="color: #666;">No candidates to display. Upload resumes or load demo data.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # Show summary stats
    if st.session_state.get("job_info"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Candidates", len(scored))
        with col2:
            st.metric("✅ Qualified", len(qualified_candidates), delta=f"{len(qualified_candidates)/len(scored)*100:.0f}%")
        with col3:
            st.metric("❌ Disqualified", len(disqualified_candidates))
        st.divider()

    # Display level distribution for qualified candidates
    if qualified_candidates and st.session_state.get("job_info"):
        st.markdown("### 📊 Qualification Level Distribution")

        job_info = st.session_state["job_info"]
        levels = job_info.get("levels", [])

        # Count candidates per level
        level_counts = {}
        for level in levels:
            level_counts[level] = 0

        for c in qualified_candidates:
            level_name = c.get("gate_results", {}).get("level_name", "")
            if level_name in level_counts:
                level_counts[level_name] += 1

        # Display distribution
        total_qualified = len(qualified_candidates)
        dist_cols = st.columns(len(levels))

        for idx, level in enumerate(levels):
            with dist_cols[idx]:
                count = level_counts[level]
                percentage = (count / total_qualified * 100) if total_qualified > 0 else 0
                st.metric(
                    f"Level {level}",
                    f"{count} candidate{'s' if count != 1 else ''}",
                    delta=f"{percentage:.0f}%"
                )

        st.divider()

    # Display QUALIFIED candidates first
    if qualified_candidates:
        st.markdown("### ✅ Qualified Candidates")
        for c in qualified_candidates:
            # Get gate results for level info
            gate_results = c.get("gate_results", {})
            level_name = gate_results.get("level_name", "")
            level_badge = f"**Level {level_name}**" if level_name else ""

            # Create expander title with qualification badge
            title = f"✅ **#{c['rank']}** — {get_candidate_display_name(c['anon_id'])} — Score: **{c['score']}** {level_badge}"

            with st.expander(title, expanded=(c['rank'] == 1)):
                # Show qualification details
                if gate_results:
                    st.success(f"**Qualifies for Level {level_name}**")
                    edu_check = gate_results.get("education_check", {})
                    if edu_check.get("message"):
                        st.caption(f"✅ Education: {edu_check['message']}")
                    skills_check = gate_results.get("skills_check", {})
                    if skills_check.get("message"):
                        st.caption(f"✅ Skills: {skills_check['message']}")
                    st.divider()

                col_info, col_actions = st.columns([3, 1])

                with col_info:
                    # Score breakdown
                    st.markdown("**Score Breakdown:**")
                    breakdown = c.get("breakdown", {})
                    breakdown_cols = st.columns(4)
                    for i, (cat, score) in enumerate(breakdown.items()):
                        with breakdown_cols[i % 4]:
                            st.metric(cat.title(), f"{score:.1f}")

                    # Features detected
                    features = c.get("features", {})
                    st.markdown("**Skills Detected:**")
                    skills = features.get("skills", [])
                    if skills:
                        st.write(", ".join(skills))
                    else:
                        st.write("*No skills detected*")

                    st.markdown(f"**Education:** {features.get('education', 'Not detected')}")
                    st.markdown(f"**Experience:** {features.get('years_experience', 0)} years")

                    # Evidence
                    evidence = features.get("evidence_lines", {})
                    if evidence:
                        st.markdown("**Evidence Snippets:**")
                        for skill, snippet in list(evidence.items())[:3]:
                            # Bold the skill keyword in the snippet
                            snippet_formatted = snippet[:100]
                            if skill.lower() in snippet_formatted.lower():
                                import re
                                pattern = re.compile(re.escape(skill), re.IGNORECASE)
                                snippet_formatted = pattern.sub(f"**{skill}**", snippet_formatted, count=1)
                            st.markdown(f"- ...{snippet_formatted}...")

                with col_actions:
                    # Human override field
                    st.markdown("**Human Override:**")
                    override = st.text_area(
                        "Notes/adjustments",
                        key=f"override_{c['anon_id']}",
                        height=100,
                        placeholder="Add reviewer notes..."
                    )
                    if override:
                        log_record({
                            "anon_id": c["anon_id"],
                            "override": override,
                            "score": c["score"],
                            "weights": weights
                        })
                        st.success("Logged")

    # Display DISQUALIFIED candidates
    if disqualified_candidates:
        st.markdown("---")
        st.markdown("### ❌ Disqualified Candidates")
        st.warning(f"**{len(disqualified_candidates)} candidate(s) did not meet minimum qualifications**")

        for c in disqualified_candidates:
            gate_results = c.get("gate_results", {})

            # Extract primary disqualification reason
            reason = ""
            if not gate_results.get("education_check", {}).get("passed", True):
                reason = " (Education)"
            elif not gate_results.get("skills_check", {}).get("passed", True):
                reason = " (Skills)"

            # Create expander title with disqualification badge
            title = f"❌ {get_candidate_display_name(c['anon_id'])} — Score: **{c['score']}**{reason}"

            with st.expander(title, expanded=False):
                # Show disqualification reasons
                st.error("**Does Not Meet Minimum Qualifications**")

                edu_check = gate_results.get("education_check", {})
                if not edu_check.get("passed", True):
                    st.markdown(f"❌ **Education:** {edu_check.get('message', 'Does not meet requirement')}")

                skills_check = gate_results.get("skills_check", {})
                if not skills_check.get("passed", True):
                    st.markdown(f"❌ **Skills:** {skills_check.get('message', 'Missing required skills')}")

                st.divider()

                col_info, col_actions = st.columns([3, 1])

                with col_info:
                    # Show what they DO have
                    features = c.get("features", {})
                    st.markdown("**Candidate Profile:**")
                    st.markdown(f"**Education:** {features.get('education', 'Not detected')}")
                    st.markdown(f"**Experience:** {features.get('years_experience', 0)} years")

                    st.markdown("**Skills Detected:**")
                    skills = features.get("skills", [])
                    if skills:
                        st.write(", ".join(skills))
                    else:
                        st.write("*No skills detected*")

                with col_actions:
                    st.markdown("**Reviewer Notes:**")
                    override = st.text_area(
                        "Optional notes",
                        key=f"override_{c['anon_id']}",
                        height=100,
                        placeholder="Add notes if reconsidering..."
                    )
                    if override:
                        log_record({
                            "anon_id": c["anon_id"],
                            "override": override,
                            "disqualified": True,
                            "reason": gate_results
                        })
                        st.success("Logged")

# =============================================================================
# TOP CANDIDATE DETAILS
# =============================================================================

if qualified_candidates:
    st.markdown("---")
    st.subheader("4. Top Candidate Analysis")
    st.caption("Compare the top 3 qualified candidates side by side")

    # Get top 3 qualified candidates
    top_candidates = qualified_candidates[:min(3, len(qualified_candidates))]

    # Create tabs based on number of candidates
    tab_names = [get_candidate_display_name(c['anon_id']) for c in top_candidates]
    tabs = st.tabs(tab_names)

    for idx, (tab, candidate) in enumerate(zip(tabs, top_candidates)):
        with tab:
            col_top1, col_top2 = st.columns([2, 1])

            with col_top1:
                st.markdown(f"**Rank:** #{candidate['rank']} | **Score:** {candidate['score']}")

                # Show qualification level
                gate_results = candidate.get("gate_results", {})
                level_name = gate_results.get("level_name", "")
                if level_name:
                    st.success(f"Qualifies for Level {level_name}")

                # Interview Questions (Template)
                st.markdown("#### Interview Questions")
                tmpl_qs = generate_template_questions(
                    candidate.get("features", {}),
                    st.session_state.get("job_text", ""),
                    candidate.get("gate_results")
                )
                for i, q in enumerate(tmpl_qs, 1):
                    st.markdown(f"{i}. {q}")

            with col_top2:
                st.markdown("#### Downloads")

                # Text summary
                summary_text = f"""Candidate Evaluation Summary
=============================
Candidate: {get_candidate_display_name(candidate['anon_id'])}
Technical ID: {candidate['anon_id']}
Rank: #{candidate['rank']}
Score: {candidate['score']}

Breakdown:
{json.dumps(candidate.get('breakdown', {}), indent=2)}

Skills: {', '.join(candidate.get('features', {}).get('skills', []))}
Education: {candidate.get('features', {}).get('education', 'N/A')}
Experience: {candidate.get('features', {}).get('years_experience', 0)} years

---
DEMO ONLY - Not for real hiring decisions.
Generated by CandidateCompass.
"""
                st.download_button(
                    "Download Summary (TXT)",
                    summary_text,
                    file_name=f"decision_{candidate['anon_id']}.txt",
                    mime="text/plain",
                    key=f"dl_txt_{idx}"
                )

                # PDF summary
                display_name = get_candidate_display_name(candidate['anon_id'])
                pdf_bytes = generate_decision_pdf(
                    candidate,
                    st.session_state.get("job_text", ""),
                    display_name
                )
                if pdf_bytes:
                    st.download_button(
                        "Download Summary (PDF)",
                        pdf_bytes,
                        file_name=f"decision_{candidate['anon_id']}.pdf",
                        mime="application/pdf",
                        key=f"dl_pdf_{idx}"
                    )

# =============================================================================
# DOWNLOADS & AUDIT
# =============================================================================

st.markdown("---")
st.subheader("5. Export & Audit")

col_exp1, col_exp2, col_exp3 = st.columns(3)

with col_exp1:
    if scored:
        csv_data = get_logs_csv(scored, st.session_state.get("candidate_display_names", {}))
        st.download_button(
            "Download Scores CSV",
            csv_data,
            file_name="candidate_scores.csv",
            mime="text/csv",
            help="Anonymized scores for all candidates"
        )

with col_exp2:
    if scored and st.button("Run Bias Audit"):
        report = bias_audit_stub(scored)
        st.json(report)
        st.download_button(
            "Download Audit Report (JSON)",
            json.dumps(report, indent=2),
            file_name="bias_audit.json",
            mime="application/json"
        )

with col_exp3:
    st.markdown("**Responsible AI Notes:**")
    st.markdown("""
    - All data anonymized on upload
    - PII mappings kept in-memory only
    - Human override required for decisions
    - No demographic data collected
    """)

# =============================================================================
# WHAT'S NEXT GUIDANCE
# =============================================================================

if scored and len(qualified_candidates) > 0:
    st.markdown("---")
    st.subheader("6. What's Next?")

    col_next1, col_next2, col_next3 = st.columns(3)

    with col_next1:
        st.markdown("#### 📞 **Schedule Interviews**")
        st.markdown("""
        - Review interview questions for top candidates
        - Coordinate with hiring panel
        - Prepare evaluation rubrics
        - Schedule video/phone screens
        """)

    with col_next2:
        st.markdown("#### 📋 **Human Review Required**")
        st.markdown("""
        - Verify AI-extracted qualifications
        - Review original resumes for context
        - Check references
        - Confirm work authorization
        """)

    with col_next3:
        st.markdown("#### 🎯 **Next Steps Checklist**")
        st.markdown("""
        - [ ] Download candidate summaries
        - [ ] Export scores CSV for records
        - [ ] Run bias audit report
        - [ ] Document hiring decisions
        """)

    st.markdown(
        f"""
        <div style="background-color: {BRANDING['secondaryBackgroundColor']};
                    border-left: 4px solid {BRANDING['purpleColor']};
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">💡</span>
                <strong>Reminder:</strong>
            </div>
            <p style="margin: 0.5rem 0 0 2rem; color: #666;">
                This tool provides decision support only. Final hiring decisions must be made by qualified human reviewers in compliance with employment laws.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: #666; font-size: 0.85rem;">
        <strong>CandidateCompass</strong> |
        Navigate Talent, Focus on Mission |
        <span style="color: {BRANDING['primaryColor']};">AI-assisted, human-reviewed</span>
    </div>
    """,
    unsafe_allow_html=True
)
