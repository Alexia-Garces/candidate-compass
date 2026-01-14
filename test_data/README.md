# CandidateCompass Test Data Suite

## Overview
Comprehensive test suite for validating CandidateCompass functionality including upload features, qualification gating, scoring, ranking, and edge case handling.

## Directory Structure

```
test_data/
├── README.md                          # This file
├── QUICK_REFERENCE.md                 # Quick lookup for expected results
├── TESTING_GUIDE.md                   # Detailed testing instructions
├── test_group_1_entry_admin/         # Entry-level administrative position
│   ├── job_admin_assistant_I_II.pdf
│   ├── resume_qualified_level_II_sarah_mitchell.pdf
│   ├── resume_qualified_level_I_james_rodriguez.pdf
│   ├── resume_edge_case_exactly_1yr_maria_chen.pdf
│   ├── resume_edge_case_missing_customer_service_david_park.pdf
│   └── resume_unqualified_insufficient_experience_alex_thompson.pdf
└── test_group_2_mid_it/              # Mid-level IT specialist position
    ├── job_it_specialist_II_IV.pdf
    ├── resume_qualified_level_IV_michael_anderson.pdf
    ├── resume_qualified_level_III_jennifer_lee.pdf
    ├── resume_qualified_level_II_education_sub_robert_martinez.pdf
    ├── resume_unqualified_no_linux_emily_white.pdf
    └── resume_unqualified_only_2yrs_daniel_brown.pdf
```

## Quick Start

### Run Test Group 1 (Entry-Level Admin)
```bash
# 1. Launch the application
python3 -m streamlit run streamlit_app.py

# 2. In the browser:
#    - Select "Upload Custom Job" from dropdown
#    - Upload: test_data/test_group_1_entry_admin/job_admin_assistant_I_II.pdf
#    - Click "Load Demo Resumes"
#    - Select all 5 resume PDFs from test_group_1_entry_admin/
#    - Review results in Section 3

# Expected Results:
#   ✅ 3 Qualified: Sarah Mitchell (Level II), James Rodriguez (Level I), Maria Chen (Level I)
#   ❌ 2 Disqualified: David Park (Skills), Alex Thompson (Experience)
```

### Run Test Group 2 (Mid-Level IT)
```bash
# Same process as above, but use test_group_2_mid_it/ files

# Expected Results:
#   ✅ 3 Qualified: Michael Anderson (Level IV), Jennifer Lee (Level III), Robert Martinez (Level II)
#   ❌ 2 Disqualified: Emily White (Skills - no Linux), Daniel Brown (Experience - only 2 yrs)
```

## What Each Test Group Validates

### Test Group 1: Entry-Level Administrative Assistant
**Validates**:
- Basic qualification gating (education, skills, tools)
- Multi-level positions (Level I vs Level II)
- Exact threshold testing (candidate with exactly 1.0 year)
- Missing required skill detection
- Insufficient experience handling

**Edge Cases**:
- Maria Chen: Exactly 1 year experience (tests `>=` vs `>`)
- David Park: Missing "customer service" keyword

### Test Group 2: Mid-Level IT Specialist
**Validates**:
- Higher education requirements (Bachelor's degree)
- Education substitution (year-for-year)
- Three-level positions (II, III, IV)
- Technical skills detection (Linux/Unix, network tools)
- Skills vs experience mismatches

**Edge Cases**:
- Robert Martinez: Education substitution (Associate's + 7 yrs → Level II)
- Emily White: Strong Windows admin, missing Linux/Unix
- Daniel Brown: All skills + certs, but only 2 years experience

## Documentation Files

### 1. QUICK_REFERENCE.md
**Use when**: You need a fast lookup of expected results

**Contains**:
- Summary tables for each test group
- Expected rankings
- Pass/fail predictions
- Edge case one-liners

**Best for**: Quick validation during workshop demos

### 2. TESTING_GUIDE.md
**Use when**: You need detailed testing instructions

**Contains**:
- Complete candidate profiles
- Step-by-step testing procedures
- Expected scores and breakdowns
- Edge case explanations
- Troubleshooting guide

**Best for**: Thorough validation and bug investigation

### 3. README.md (this file)
**Use when**: You need an overview of the test suite

**Contains**:
- Directory structure
- Quick start commands
- Test data statistics
- File naming conventions

**Best for**: Onboarding and reference

## Test Data Statistics

| Metric | Count |
|--------|-------|
| Total PDFs | 12 |
| Job Descriptions | 2 |
| Candidate Resumes | 10 |
| Qualified Candidates | 6 |
| Disqualified Candidates | 4 |
| Edge Cases | 4 |
| Test Groups | 2 (with 2 more planned) |

## Expected Test Results Summary

### Qualified Candidates (6 total)
1. **Sarah Mitchell** (Test Group 1) - Level II, 4 years
2. **James Rodriguez** (Test Group 1) - Level I, 1.5 years
3. **Maria Chen** (Test Group 1) - Level I, 1.0 year ⚠️ *Edge*
4. **Michael Anderson** (Test Group 2) - Level IV, 8 years
5. **Jennifer Lee** (Test Group 2) - Level III, 5 years
6. **Robert Martinez** (Test Group 2) - Level II, education sub ⚠️ *Edge*

### Disqualified Candidates (4 total)
1. **David Park** (Test Group 1) - Missing customer service ⚠️ *Edge*
2. **Alex Thompson** (Test Group 1) - Only 0.5 years
3. **Emily White** (Test Group 2) - Missing Linux/Unix ⚠️ *Edge*
4. **Daniel Brown** (Test Group 2) - Only 2 years (skills strong)

## File Naming Convention

All resume files follow this pattern:
```
resume_[status]_[details]_[firstname_lastname].pdf
```

**Status Categories**:
- `qualified_level_X` - Passes gating, qualifies for Level X
- `edge_case_[issue]` - Boundary/edge case scenario
- `unqualified_[reason]` - Fails gating due to specific reason

**Examples**:
- `resume_qualified_level_II_sarah_mitchell.pdf`
- `resume_edge_case_exactly_1yr_maria_chen.pdf`
- `resume_unqualified_no_linux_emily_white.pdf`

## How Test Data Was Generated

Test PDFs were programmatically generated using `generate_test_data.py`:

```bash
python3 generate_test_data.py
```

**Generation Features**:
- Realistic government job descriptions
- Multi-page candidate resumes
- Proper formatting with ReportLab
- Consistent structure across all files
- Strategic keyword placement for testing

**Customization**: Edit `generate_test_data.py` to create additional test groups or modify existing ones.

## Common Testing Scenarios

### Scenario 1: Validate Qualification Gating
**Test**: Upload Test Group 1
**Check**: Exactly 3 qualified, 2 disqualified
**Why**: Ensures basic pass/fail logic works

### Scenario 2: Validate Level Assignment
**Test**: Upload Test Group 2
**Check**: Michael=IV, Jennifer=III, Robert=II
**Why**: Ensures experience thresholds assign correct levels

### Scenario 3: Validate Edge Cases
**Test**: Upload both test groups
**Check**: Maria passes (1.0 yr), David fails (missing skill), Robert gets Level II (not IV)
**Why**: Ensures boundary conditions handled correctly

### Scenario 4: Validate Education Substitution
**Test**: Upload Test Group 2, focus on Robert Martinez
**Check**: Qualified for Level II despite lacking Bachelor's
**Why**: Ensures year-for-year substitution works

### Scenario 5: Validate Ranking Logic
**Test**: Upload Test Group 1
**Check**: Sarah ranks above James, James above Maria
**Why**: Ensures scoring produces logical rankings

## Troubleshooting

### Issue: Wrong number of qualified candidates
**Solution**: Check TESTING_GUIDE.md for expected counts and reasons

### Issue: Candidate at wrong level
**Solution**: Review education substitution logic in TESTING_GUIDE.md

### Issue: Unexpected disqualification
**Solution**: Expand candidate card to see gate results, check which skill/requirement failed

### Issue: Keywords not detected
**Solution**: Check if resume uses different phrasing (e.g., "Linux" vs "Linux/Unix")

## Future Test Groups (Planned)

### Test Group 3: Senior Project Manager
**Focus**: Complex education substitution, soft skills, certifications

### Test Group 4: Multi-Level Position (I, III, V)
**Focus**: Non-consecutive levels, larger experience gaps

## Contributing

To add new test groups:

1. Create new directory: `test_data/test_group_X_description/`
2. Update `generate_test_data.py` with new generation function
3. Run generator: `python3 generate_test_data.py`
4. Add expected results to TESTING_GUIDE.md
5. Update this README with new test group info

## Questions or Issues?

1. Check QUICK_REFERENCE.md for expected results
2. Review TESTING_GUIDE.md for detailed explanations
3. Verify you're using correct job + resume combinations
4. Check application logs for errors

---

**Last Updated**: January 2026
**Version**: 1.0
**Test Data Generator**: generate_test_data.py
