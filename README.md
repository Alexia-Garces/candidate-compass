# Candidate Ranker — Demo

Staff-Augmentation Candidate Ranker optimized for a **15-minute workshop** with 10 participants. Built with public-sector responsible AI guardrails.

## Features

- **Upload & Anonymize**: Accept job description PDF + multiple resume PDFs; immediate PII anonymization
- **Smart Scoring**: Extract features, score & rank via editable rubric (sliders)
- **Interview Questions**: Template questions always available; optional AI-assisted drafting
- **Human Oversight**: Override fields for reviewer notes on each candidate
- **Export & Audit**: CSV logs, decision summary (TXT/PDF), bias audit stub
- **Privacy First**: All data in-memory only; purgeable with one click

## Quick Start

```bash
# 1. Clone and enter directory
cd streamlit-candidate-ranker

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
streamlit-candidate-ranker/
├── streamlit_app.py          # Main Streamlit application
├── utils.py                  # Anonymization, scoring, questions, PDF generation
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration
├── assets/
│   ├── logo.png              # Header logo
│   ├── CGI_logo_*.png/svg    # Logo variants
│   ├── favicon.ico           # Browser favicon
│   ├── brand_guide.md        # Branding documentation
│   └── gradients/
│       └── header-gradient.svg  # Header gradient background
├── sample_data/
│   └── generated/
│       └── ExampleJob/
│           ├── job.txt       # Example job description
│           └── *.pdf         # Example anonymized resumes
├── tests/
│   └── test_utils.py         # Unit tests
└── README.md                 # This file
```

## Branding Customization

### Changing Colors

Edit the `BRANDING` dictionary in `streamlit_app.py`:

```python
BRANDING = {
    "primaryColor": "#E31937",          # Main accent color
    "textColor": "#333333",              # Body text
    "backgroundColor": "#FFFFFF",        # Main background
    "secondaryBackgroundColor": "#F3F6F9",  # Sidebar/cards
    ...
}
```

Also update `.streamlit/config.toml` to match.

### Replacing Logo

1. Add your logo to `assets/` (PNG or SVG, 200-400px wide recommended)
2. Update `BRANDING["logo_path"]` in `streamlit_app.py`
3. For gradient backgrounds, use a white/light logo variant

### Replacing Gradient

1. Create SVG or PNG (1920×200 recommended)
2. Save as `assets/gradients/header-gradient.svg`
3. Or modify `BRANDING["gradient_css_fallback"]` for pure CSS

See `assets/brand_guide.md` for complete documentation.

## 15-Minute Facilitator Flow

### Preparation (Before Workshop)
- [ ] Verify app runs: `streamlit run streamlit_app.py`
- [ ] Test "Load Demo Data" button
- [ ] Prepare screen share

### Workshop Agenda

| Time | Activity | Notes |
|------|----------|-------|
| 0:00 | **Introduction** (2 min) | Explain purpose: AI-assisted screening with human oversight |
| 2:00 | **Load Demo Data** (1 min) | Click button, show 5 candidates loaded |
| 3:00 | **Scoring Rubric** (3 min) | Adjust sliders, show rankings update in real-time |
| 6:00 | **Review Top Candidate** (3 min) | Expand details, show evidence snippets, skills detected |
| 9:00 | **Interview Questions** (2 min) | Show template questions tailored to candidate level |
| 11:00 | **Human Override** (2 min) | Add notes to a candidate, explain audit trail |
| 13:00 | **Export & Bias Audit** (1 min) | Download CSV, run bias audit |
| 14:00 | **Q&A / Wrap-up** (1 min) | Emphasize: demo only, human decisions required |

### Key Talking Points

1. **Anonymization**: "All PII is stripped immediately on upload"
2. **Transparency**: "Scores are explainable - see the breakdown and evidence"
3. **Human Control**: "You adjust the rubric; you make the final decision"
4. **Responsible AI**: "No demographic data collected; bias audit available"
5. **Demo Limitations**: "This is for illustration - not production hiring"

## Running Tests

```bash
pytest tests/test_utils.py -v
```

## Deployment

### Streamlit Community Cloud

1. Push repo to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]
```

## Accessibility & Contrast

The app includes a contrast ratio checker (`utils.check_contrast_ratio()`) that:
- Calculates WCAG 2.1 relative luminance
- Logs warnings if contrast < 4.5:1
- Runs automatically on header render

Check console output for any contrast warnings.

## Responsible AI Guardrails

| Guardrail | Implementation |
|-----------|----------------|
| PII Protection | Regex-based anonymization on all uploads |
| Data Minimization | In-memory only; no persistence |
| Transparency | Explainable scores with evidence snippets |
| Human Oversight | Override fields; final decisions by humans |
| Bias Awareness | Audit stub; no demographic profiling |
| Purpose Limitation | Clear "DEMO ONLY" banner throughout |

## License

Demo / Educational Use Only. Not for production hiring decisions.

## Support

For issues or feedback: [Open an issue](https://github.com/your-org/streamlit-candidate-ranker/issues)
