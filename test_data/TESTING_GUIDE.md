# CandidateCompass Testing Guide
**Comprehensive Test Plan for Upload Functionality & Edge Cases**

## Overview
This testing guide provides detailed instructions for validating the CandidateCompass application using realistic government job descriptions and candidate resumes. Each test group includes expected results to help you verify the application is working correctly.

---

## Test Data Organization

```
test_data/
├── test_group_1_entry_admin/     # Entry-level administrative position
├── test_group_2_mid_it/           # Mid-level IT specialist position
├── test_group_3_senior_pm/        # Senior project manager (TBD)
├── test_group_4_multilevel/       # Multi-level position (TBD)
└── TESTING_GUIDE.md              # This file
```

---

## How to Run Tests

### Step 1: Launch CandidateCompass
```bash
python3 -m streamlit run streamlit_app.py
```

### Step 2: Upload Custom Job & Resumes
1. In Section 1, select **"Upload Custom Job"** from the dropdown
2. Upload the job description PDF for your test group
3. In Section 2, click **"Load Demo Resumes"** and select all resume PDFs for that test group
4. Proceed to Section 3 to view scored and ranked candidates

### Step 3: Verify Results
Compare the application's output against the expected results documented below.

---

## TEST GROUP 1: Entry-Level Administrative Assistant I-II

### Job Requirements Summary
- **Title**: Administrative Assistant I-II
- **Agency**: Department of General Services
- **Required Education**: High School Diploma or GED (Associate's preferred)
- **Required Skills** (must have ALL):
  - Microsoft Office Suite (Word, Excel, Outlook)
  - Data entry and record keeping
  - Customer service
  - Written and verbal communication
- **Required Tools** (must have at least ONE):
  - QuickBooks
  - SAP
  - Oracle Financials
- **Experience Levels**:
  - Level I: 1+ years
  - Level II: 3+ years

### Test Cases

#### Candidate 1: Sarah Mitchell ✅ QUALIFIED Level II
**File**: `resume_qualified_level_II_sarah_mitchell.pdf`

**Profile**:
- Education: Associate's degree (exceeds requirement)
- Experience: 4 years
- Skills: ALL required skills ✓
- Tools: QuickBooks ✓

**Expected Results**:
- ✅ **Should PASS qualification gating**
- ✅ **Qualifies for Level II** (has 4 years, needs 3+)
- ✅ **Should rank #1 or #2** (strongest candidate)
- **Expected Score**: 75-85 points
- **Education Score**: High (has Associate's)
- **Experience Score**: High (4 years)
- **Skills Score**: High (all required + extras)

**Validation Checklist**:
- [ ] Candidate appears in "Qualified Candidates" section
- [ ] Level badge shows "Level II"
- [ ] Evidence snippets mention QuickBooks, Microsoft Office, customer service
- [ ] Interview questions reference administrative coordination experience

---

#### Candidate 2: James Rodriguez ✅ QUALIFIED Level I
**File**: `resume_qualified_level_I_james_rodriguez.pdf`

**Profile**:
- Education: High School Diploma + certificate in progress
- Experience: 1.5 years
- Skills: ALL required skills ✓
- Tools: SAP (basic) ✓

**Expected Results**:
- ✅ **Should PASS qualification gating**
- ✅ **Qualifies for Level I** (has 1.5 years, needs 1+, but < 3 for Level II)
- ✅ **Should rank #3-#4** (qualified but less experience)
- **Expected Score**: 55-65 points
- **Education Score**: Moderate (meets minimum)
- **Experience Score**: Low-Moderate (1.5 years)
- **Skills Score**: Moderate (all required but fewer extras)

**Validation Checklist**:
- [ ] Candidate appears in "Qualified Candidates" section
- [ ] Level badge shows "Level I"
- [ ] Evidence snippets mention SAP, data entry, Microsoft Office
- [ ] Experience listed as ~1.5 years

---

#### Candidate 3: Maria Chen ⚠️ EDGE CASE - Exactly 1 Year
**File**: `resume_edge_case_exactly_1yr_maria_chen.pdf`

**Profile**:
- Education: Associate's degree
- Experience: **EXACTLY 1 year** (12 months)
- Skills: ALL required skills ✓
- Tools: Oracle Financials ✓

**Expected Results**:
- ✅ **Should PASS qualification gating** (meets Level I threshold)
- ✅ **Qualifies for Level I** (exactly 1 year meets 1+ requirement)
- ✅ **Should rank #4-#5** (minimum experience)
- **Expected Score**: 50-60 points
- **Education Score**: High (has Associate's)
- **Experience Score**: Low (only 1 year - at minimum)
- **Skills Score**: Moderate-High

**Edge Case Testing**:
- **Critical**: Verify the system accepts exactly 1 year as meeting "1+ years" requirement
- [ ] Does NOT appear in "Disqualified" section
- [ ] Experience parsing recognizes "12 months" = 1 year
- [ ] Level badge shows "Level I"

**Known Issues to Watch For**:
- If system uses `>` instead of `>=` for experience check, this candidate will incorrectly fail
- If date parsing rounds down, may show as 0 years

---

#### Candidate 4: David Park ⚠️ EDGE CASE - Missing "Customer Service"
**File**: `resume_edge_case_missing_customer_service_david_park.pdf`

**Profile**:
- Education: High School Diploma
- Experience: 3 years
- Skills: Has Microsoft Office, Data Entry, Written/Verbal Communication
- **MISSING**: "Customer Service" (not mentioned anywhere in resume)
- Tools: QuickBooks ✓

**Expected Results**:
- ❌ **Should FAIL qualification gating** (missing required skill)
- ❌ **Should appear in "Disqualified Candidates" section**
- ❌ **Disqualification reason: (Skills)**
- **Expected Score**: May still show moderate score (60-70), but disqualified

**Edge Case Testing**:
- **Critical**: Verify the system correctly identifies missing "customer service" skill
- [ ] Appears in "Disqualified Candidates" section with red ❌
- [ ] Title shows "(Skills)" as disqualification reason
- [ ] Gate results explain which skill is missing

**What Makes This Tricky**:
- Candidate has 3 years experience (would qualify for Level II)
- Has most other required skills and tools
- Strong on paper but missing one critical skill
- Tests keyword matching accuracy

---

#### Candidate 5: Alex Thompson ❌ UNQUALIFIED - Insufficient Experience
**File**: `resume_unqualified_insufficient_experience_alex_thompson.pdf`

**Profile**:
- Education: High School Diploma only
- Experience: Only 0.5 years (6 months)
- Skills: Limited - only basic Microsoft Office
- Tools: NONE (no QuickBooks, SAP, or Oracle)

**Expected Results**:
- ❌ **Should FAIL qualification gating** (insufficient experience + missing skills/tools)
- ❌ **Should appear in "Disqualified Candidates" section**
- ❌ **Disqualification reason: (Skills) or (Education)** depending on order checked
- **Expected Score**: Low (30-40 points)

**Validation Checklist**:
- [ ] Appears in "Disqualified Candidates" section
- [ ] Experience shown as < 1 year
- [ ] Gate results show multiple failures (experience, possibly skills)
- [ ] Should rank last among all candidates

---

### Test Group 1 Summary Table

| Candidate | Education | Experience | All Skills? | Tool? | Expected Result | Expected Level |
|-----------|-----------|------------|-------------|-------|-----------------|----------------|
| Sarah Mitchell | Associate's ✓ | 4 years | ✓ | QuickBooks | ✅ QUALIFIED | Level II |
| James Rodriguez | HS Diploma ✓ | 1.5 years | ✓ | SAP | ✅ QUALIFIED | Level I |
| Maria Chen | Associate's ✓ | **1.0 year** | ✓ | Oracle | ⚠️ EDGE (1yr exact) | Level I |
| David Park | HS Diploma ✓ | 3 years | ❌ No Cust Svc | QuickBooks | ❌ DISQUALIFIED | (Skills) |
| Alex Thompson | HS Diploma ✓ | 0.5 years | ❌ Missing | ❌ None | ❌ DISQUALIFIED | (Multiple) |

### Expected Ranking (Qualified Only)
1. **Sarah Mitchell** (Level II, 4 years, Associate's)
2. **James Rodriguez** (Level I, 1.5 years)
3. **Maria Chen** (Level I, exactly 1 year, edge case)

---

## TEST GROUP 2: Mid-Level IT Specialist II-IV

### Job Requirements Summary
- **Title**: IT Specialist II-IV (Network Administration)
- **Agency**: Department of Information Technology
- **Required Education**: Bachelor's in CS/IT (or equivalent experience on year-for-year basis)
- **Required Skills** (must have ALL):
  - Network administration
  - Windows Server
  - Linux/Unix
  - TCP/IP protocols
  - Network security
- **Required Tools** (must have at least ONE):
  - Cisco routers
  - Juniper networks
  - Fortinet firewalls
  - Palo Alto firewalls
- **Experience Levels**:
  - Level II: 3+ years
  - Level III: 5+ years
  - Level IV: 7+ years

### Test Cases

#### Candidate 1: Michael Anderson ✅ QUALIFIED Level IV
**File**: `resume_qualified_level_IV_michael_anderson.pdf`

**Profile**:
- Education: Bachelor's degree ✓
- Experience: 8 years
- Skills: ALL required skills ✓ (plus extras)
- Tools: Cisco, Fortinet, Palo Alto ✓✓✓
- Certifications: CCNP, Security+, Windows Server cert

**Expected Results**:
- ✅ **Should PASS qualification gating**
- ✅ **Qualifies for Level IV** (has 8 years, needs 7+)
- ✅ **Should rank #1** (most experienced, best qualified)
- **Expected Score**: 85-95 points (highest score)
- **Education Score**: High (Bachelor's degree)
- **Experience Score**: Very High (8 years, but capped at 15)
- **Skills Score**: Very High (all required + many extras)
- **Certifications Score**: High (CCNP, Security+)

**Validation Checklist**:
- [ ] Candidate appears at top of "Qualified Candidates" section
- [ ] Level badge shows "Level IV"
- [ ] Evidence snippets mention multiple tools (Cisco, Fortinet, Palo Alto)
- [ ] Interview questions reference senior-level responsibilities

---

#### Candidate 2: Jennifer Lee ✅ QUALIFIED Level III
**File**: `resume_qualified_level_III_jennifer_lee.pdf`

**Profile**:
- Education: Bachelor's in IT ✓
- Experience: 5 years
- Skills: ALL required skills ✓
- Tools: Cisco, Fortinet ✓✓
- Certifications: CCNA, Network+

**Expected Results**:
- ✅ **Should PASS qualification gating**
- ✅ **Qualifies for Level III** (has 5 years, needs 5+, but < 7 for Level IV)
- ✅ **Should rank #2** (strong candidate, mid-level)
- **Expected Score**: 70-80 points
- **Education Score**: High (Bachelor's degree)
- **Experience Score**: Moderate-High (5 years)
- **Skills Score**: High (all required)

**Validation Checklist**:
- [ ] Candidate appears in "Qualified Candidates" section
- [ ] Level badge shows "Level III"
- [ ] Evidence snippets mention Cisco, Fortinet
- [ ] Experience listed as 5 years

---

#### Candidate 3: Robert Martinez ✅ QUALIFIED Level II (Education Substitution)
**File**: `resume_qualified_level_II_education_sub_robert_martinez.pdf`

**Profile**:
- Education: **Associate's degree only** (NOT Bachelor's)
- Experience: **7 years total experience**
- Skills: ALL required skills ✓
- Tools: Cisco, Juniper ✓✓
- Certifications: Network+, Security+

**Expected Results**:
- ✅ **Should PASS qualification gating** (education substitution applies)
- ✅ **Qualifies for Level II** (education substitution logic)
- ✅ **Should rank #3** (qualified but education substitution case)
- **Expected Score**: 65-75 points
- **Education Score**: Moderate-Low (only Associate's, not Bachelor's)
- **Experience Score**: High (7 years)
- **Skills Score**: High (all required)

**Education Substitution Logic**:
- Job requires: Bachelor's degree (4 years) + 3 years experience = 7 years total for Level II
- Candidate has: Associate's (2 years) + 7 years experience = 9 years total
- **Calculation**: 7 years experience - 4 years (missing education) = 3 effective years
- **Result**: Qualifies for Level II (needs 3+ years)

**Edge Case Testing**:
- **Critical**: Verify education substitution is correctly calculated
- [ ] Candidate appears in "Qualified Candidates" section (not disqualified for education)
- [ ] Education check shows PASS with substitution note
- [ ] Level badge shows "Level II" (not Level IV despite 7 years actual experience)

---

#### Candidate 4: Emily White ❌ UNQUALIFIED - Missing Linux/Unix
**File**: `resume_unqualified_no_linux_emily_white.pdf`

**Profile**:
- Education: Bachelor's degree ✓
- Experience: 4 years
- Skills: Has Windows Server, TCP/IP, Network Admin, Network Security
- **MISSING**: Linux/Unix (not mentioned)
- Tools: Cisco, Fortinet ✓✓

**Expected Results**:
- ❌ **Should FAIL qualification gating** (missing required skill)
- ❌ **Should appear in "Disqualified Candidates" section**
- ❌ **Disqualification reason: (Skills)**
- **Expected Score**: May show 60-70 points, but disqualified

**Edge Case Testing**:
- **Critical**: Verify system detects missing "Linux/Unix" or "Linux" keyword
- [ ] Appears in "Disqualified Candidates" section
- [ ] Title shows "(Skills)" as disqualification reason
- [ ] Gate results explain "Linux/Unix" skill is missing

**What Makes This Tricky**:
- Candidate is strong in Windows environments
- Has 4 years experience (would qualify for Level II if had all skills)
- Tests whether system requires multi-platform experience
- Common real-world scenario: Windows-only admins applying for multi-platform roles

---

#### Candidate 5: Daniel Brown ❌ UNQUALIFIED - Insufficient Experience
**File**: `resume_unqualified_only_2yrs_daniel_brown.pdf`

**Profile**:
- Education: Bachelor's degree ✓
- Experience: Only 2 years
- Skills: ALL required skills ✓ (impressive skill set!)
- Tools: Cisco, Palo Alto, Juniper ✓✓✓
- Certifications: CCNA, Security+, Linux+

**Expected Results**:
- ❌ **Should FAIL qualification gating** (insufficient experience for Level II)
- ❌ **Should appear in "Disqualified Candidates" section**
- ❌ **Disqualification reason: Experience (needs 3+ years for Level II)**
- **Expected Score**: May show 65-75 points (strong skills/certs), but disqualified

**Edge Case Testing**:
- **Critical**: Verify experience threshold is enforced even when skills are strong
- [ ] Appears in "Disqualified Candidates" section
- [ ] Experience listed as 2 years
- [ ] Gate results show failure on experience requirement
- [ ] System recognizes candidate has all required skills but still fails on experience

**What Makes This Tricky**:
- Recent graduate with excellent academic skills
- Has ALL required technical skills
- Multiple certifications
- Tests whether system enforces experience minimums strictly
- Realistic scenario: overqualified on skills, underqualified on experience

---

### Test Group 2 Summary Table

| Candidate | Education | Experience | All Skills? | Tool? | Expected Result | Expected Level |
|-----------|-----------|------------|-------------|-------|-----------------|----------------|
| Michael Anderson | Bachelor's ✓ | 8 years | ✓ | Cisco/Fortinet/PA | ✅ QUALIFIED | Level IV |
| Jennifer Lee | Bachelor's ✓ | 5 years | ✓ | Cisco/Fortinet | ✅ QUALIFIED | Level III |
| Robert Martinez | Associate's | 7 years | ✓ | Cisco/Juniper | ⚠️ EDGE (Ed Sub) | Level II |
| Emily White | Bachelor's ✓ | 4 years | ❌ No Linux | Cisco/Fortinet | ❌ DISQUALIFIED | (Skills) |
| Daniel Brown | Bachelor's ✓ | **2 years** | ✓ | Cisco/PA/Juniper | ❌ DISQUALIFIED | (Experience) |

### Expected Ranking (Qualified Only)
1. **Michael Anderson** (Level IV, 8 years, all certifications)
2. **Jennifer Lee** (Level III, 5 years, strong background)
3. **Robert Martinez** (Level II, education substitution case)

---

## Edge Case Reference Guide

### 1. Exact Threshold Experience (Maria Chen - Test Group 1)
**Scenario**: Candidate has exactly 1 year of experience when requirement is "1+ years"

**What to Test**:
- System correctly identifies 1.0 years as meeting >= 1 requirement
- Date parsing recognizes "12 months" as equivalent to "1 year"
- Candidate does NOT appear in disqualified section

**Common Bugs**:
- Using `>` instead of `>=` for threshold check
- Rounding errors in date calculation
- Off-by-one errors in year counting

---

### 2. Missing Single Required Skill (David Park, Emily White)
**Scenario**: Candidate meets most requirements but is missing ONE required skill

**What to Test**:
- System correctly identifies the missing skill
- Candidate is disqualified even if strong in other areas
- Disqualification reason clearly states "(Skills)"
- Gate results detail which specific skill is missing

**Common Bugs**:
- Partial matching (e.g., accepting "service" when "customer service" is required)
- Missing skills not clearly reported
- System allows candidate to pass if they have "most" skills

---

### 3. Education Substitution (Robert Martinez - Test Group 2)
**Scenario**: Candidate lacks required degree but has extra years of experience

**What to Test**:
- System applies year-for-year substitution correctly
- Bachelor's degree (4 years) can be substituted by 4 years experience
- Effective experience calculation: actual_experience - missing_education_years
- Level determination uses effective experience, not raw experience

**Calculation Example**:
```
Job requires: Bachelor's (4 yrs) + 3 yrs exp = Level II
Candidate has: Associate's (2 yrs) + 7 yrs exp
Missing education: 4 - 2 = 2 years
Effective experience: 7 - 2 = 5 years
Result: 5 years effective ≥ 3 years required → QUALIFIED for Level II
```

**Common Bugs**:
- Not applying substitution at all (candidate wrongly disqualified)
- Incorrect math in substitution calculation
- Assigning wrong level based on raw vs. effective experience

---

### 4. Strong Skills, Weak Experience (Daniel Brown - Test Group 2)
**Scenario**: Recent graduate with excellent skills/certifications but insufficient years

**What to Test**:
- System enforces experience minimums even when skills are strong
- Candidate is disqualified despite having all required technical skills
- Experience requirement is clearly communicated in disqualification

**Common Bugs**:
- Skills score compensates for lack of experience (shouldn't)
- System accepts certifications as experience substitute (shouldn't)
- Unclear why candidate was disqualified

---

### 5. Missing Required Tool (if only "required_any_of" field missing)
**Scenario**: Candidate has all skills but doesn't mention any of the required tools

**What to Test**:
- System checks "required_any_of" field (at least ONE must be present)
- Candidate fails qualification if zero matches found
- Gate results clearly indicate which tools were required

**Note**: This edge case is not explicitly tested in current test groups but should be considered for future testing.

---

## Testing Checklist - Per Test Group

Use this checklist when testing each group:

### Before Upload
- [ ] Application is running (`streamlit run streamlit_app.py`)
- [ ] Starting from clean state (no previous data loaded)

### Upload Process
- [ ] Select "Upload Custom Job" from dropdown
- [ ] Upload job description PDF successfully
- [ ] Job requirements summary card displays correctly
- [ ] Click "Load Demo Resumes" button
- [ ] Select ALL resume PDFs for the test group
- [ ] Success message confirms number of candidates loaded

### Verification Steps
- [ ] Section 3 displays "Ranked Candidates" heading
- [ ] "Qualified Candidates" section shows expected candidates
- [ ] "Disqualified Candidates" section shows expected candidates
- [ ] Level badges are correct for qualified candidates
- [ ] Disqualification reasons are correct (Education vs. Skills)
- [ ] Ranking order matches expected order
- [ ] Score ranges are reasonable
- [ ] Evidence snippets contain relevant keywords
- [ ] "Level Distribution" metrics are accurate
- [ ] Top Candidate Analysis tabs show top 3 (or fewer if < 3 qualified)

### Export & Download Testing
- [ ] Export scores CSV includes all candidates
- [ ] CSV shows display names (Candidate A, B, C...)
- [ ] Download candidate summary PDFs for qualified candidates
- [ ] PDFs contain correct information and display names

### Edge Case Validation
- [ ] Edge case candidates behave as documented
- [ ] Exact threshold experience is handled correctly
- [ ] Missing skills are detected accurately
- [ ] Education substitution is calculated correctly

---

## Troubleshooting Guide

### Issue: Candidate unexpectedly disqualified
**Possible Causes**:
1. Keyword matching issue - check if skill is phrased differently than expected
2. Experience parsing error - check if dates are interpreted correctly
3. Education requirement too strict - verify if substitution should apply

**How to Debug**:
- Expand the candidate's card in "Disqualified Candidates"
- Check "Gate Results" section for specific failure reason
- Review "Features Detected" to see what system extracted from resume

---

### Issue: Wrong level assigned
**Possible Causes**:
1. Experience not parsed correctly from resume
2. Education substitution not applied
3. Level thresholds configured incorrectly in job

**How to Debug**:
- Check "Years of Experience" in candidate details
- Verify job requirements show correct level thresholds
- For education substitution cases, check if math is correct

---

### Issue: Ranking seems incorrect
**Possible Causes**:
1. Scoring weights not balanced appropriately
2. Experience capping (15 years) affecting senior candidates
3. Skills capping (10 points) affecting candidates with many skills

**How to Debug**:
- Review "Breakdown" section showing points per category
- Adjust scoring weights in Section 3 to test sensitivity
- Check if candidates with similar scores are ranked as expected

---

## Expected Outcomes Summary

### Test Group 1 (Entry-Level Admin)
- **Qualified**: 3 candidates (Sarah, James, Maria)
- **Disqualified**: 2 candidates (David - skills, Alex - experience)
- **Edge Cases**: Maria (exactly 1 year), David (missing 1 skill)

### Test Group 2 (Mid-Level IT)
- **Qualified**: 3 candidates (Michael, Jennifer, Robert)
- **Disqualified**: 2 candidates (Emily - no Linux, Daniel - only 2 yrs)
- **Edge Cases**: Robert (education substitution), Daniel (strong skills, weak experience)

---

## Next Steps

After validating Test Groups 1 and 2:
1. Create Test Group 3: Senior-Level Project Manager with complex edge cases
2. Create Test Group 4: Multi-level position (Levels I, III, V) to test level distribution
3. Run bias audit on test data to verify fairness metrics
4. Test CSV export and PDF generation for all candidates

---

## Questions or Issues?

If you encounter unexpected behavior:
1. Check this guide's "Troubleshooting" section
2. Verify you uploaded the correct job + resume combination
3. Expand candidate cards to review detailed gate results
4. Adjust scoring weights to understand impact on rankings

**Remember**: The goal is to verify the system correctly:
- Identifies qualified vs. disqualified candidates
- Assigns appropriate levels based on experience
- Handles edge cases (exact thresholds, education substitution, missing skills)
- Provides clear explanations for decisions
