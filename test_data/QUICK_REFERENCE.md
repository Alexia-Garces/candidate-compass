# CandidateCompass Test Data - Quick Reference Card

## Test Group 1: Entry-Level Administrative Assistant I-II

**Job File**: `test_group_1_entry_admin/job_admin_assistant_I_II.pdf`

**Quick Stats**:
- Levels: I (1+ yrs), II (3+ yrs)
- Required Education: High School Diploma
- Required Skills: 4 (Microsoft Office, Data Entry, Customer Service, Communication)
- Required Tools: 1 of 3 (QuickBooks, SAP, Oracle)

| # | Candidate | Experience | Result | Level | Why |
|---|-----------|------------|--------|-------|-----|
| 1 | Sarah Mitchell | 4 yrs | ✅ PASS | II | Perfect match - Associate's + all skills |
| 2 | James Rodriguez | 1.5 yrs | ✅ PASS | I | Entry level - meets minimum |
| 3 | Maria Chen | 1.0 yr | ⚠️ EDGE | I | **Exactly 1 year** - tests threshold |
| 4 | David Park | 3 yrs | ❌ FAIL | - | **Missing customer service skill** |
| 5 | Alex Thompson | 0.5 yrs | ❌ FAIL | - | Insufficient experience |

**Expected Ranking**: Sarah (#1) → James (#2) → Maria (#3)

---

## Test Group 2: Mid-Level IT Specialist II-IV

**Job File**: `test_group_2_mid_it/job_it_specialist_II_IV.pdf`

**Quick Stats**:
- Levels: II (3+ yrs), III (5+ yrs), IV (7+ yrs)
- Required Education: Bachelor's (or equivalent experience)
- Required Skills: 5 (Network Admin, Windows Server, Linux/Unix, TCP/IP, Network Security)
- Required Tools: 1 of 4 (Cisco, Juniper, Fortinet, Palo Alto)

| # | Candidate | Experience | Result | Level | Why |
|---|-----------|------------|--------|-------|-----|
| 1 | Michael Anderson | 8 yrs | ✅ PASS | IV | Senior - most experienced |
| 2 | Jennifer Lee | 5 yrs | ✅ PASS | III | Mid-level - strong background |
| 3 | Robert Martinez | 7 yrs | ⚠️ EDGE | II | **Education substitution** - only Associate's |
| 4 | Emily White | 4 yrs | ❌ FAIL | - | **Missing Linux/Unix** |
| 5 | Daniel Brown | 2 yrs | ❌ FAIL | - | Only 2 years (needs 3+ for Level II) |

**Expected Ranking**: Michael (#1) → Jennifer (#2) → Robert (#3)

---

## Edge Cases at a Glance

### 🔍 Exact Threshold (Maria Chen)
- Has exactly 1.0 year when 1+ required
- Tests: >= vs > in threshold checks
- Expected: Should PASS

### 🔍 Missing Single Skill (David Park, Emily White)
- All other requirements met except ONE skill
- Tests: Keyword detection accuracy
- Expected: Should FAIL with "(Skills)" reason

### 🔍 Education Substitution (Robert Martinez)
- Only Associate's, not Bachelor's
- 7 years raw → 5 years effective (after substitution)
- Tests: Year-for-year calculation
- Expected: Should PASS for Level II, not Level IV

### 🔍 Skills vs Experience Mismatch (Daniel Brown)
- Has ALL skills + certifications
- Only 2 years experience (needs 3+)
- Tests: Experience requirement enforcement
- Expected: Should FAIL despite strong skills

---

## How to Use

### Quick Test (5 minutes)
1. Launch: `python3 -m streamlit run streamlit_app.py`
2. Upload Test Group 1 job + all 5 resumes
3. Verify: 3 qualified, 2 disqualified
4. Check: Maria Chen appears in qualified (edge case)

### Full Test (15 minutes)
1. Run Test Group 1 (validate ranking & edge cases)
2. Run Test Group 2 (validate education substitution)
3. Export CSV and verify display names
4. Download PDFs for top candidates

### What to Watch For
- ✅ Qualified count matches expected
- ✅ Disqualified reasons are correct (Skills vs Experience)
- ✅ Level badges match expected levels
- ✅ Edge cases pass/fail as expected
- ✅ Ranking order is logical

---

## File Naming Convention

```
resume_[status]_[details]_[name].pdf

Status:
  - qualified_level_X
  - edge_case_[issue]
  - unqualified_[reason]
```

Examples:
- `resume_qualified_level_II_sarah_mitchell.pdf` → Clear pass
- `resume_edge_case_exactly_1yr_maria_chen.pdf` → Boundary test
- `resume_unqualified_no_linux_emily_white.pdf` → Missing skill

---

## Expected Outcomes

### Test Group 1 Success Criteria
- [ ] 3 candidates qualified (Sarah, James, Maria)
- [ ] 2 candidates disqualified (David, Alex)
- [ ] Maria Chen (1.0 year) passes threshold
- [ ] David Park fails on "customer service" skill
- [ ] Ranking: Sarah > James > Maria

### Test Group 2 Success Criteria
- [ ] 3 candidates qualified (Michael, Jennifer, Robert)
- [ ] 2 candidates disqualified (Emily, Daniel)
- [ ] Robert gets Level II (not IV) due to education sub
- [ ] Emily fails on "Linux/Unix" skill
- [ ] Daniel fails on experience (despite good skills)
- [ ] Ranking: Michael > Jennifer > Robert

---

## Troubleshooting Quick Tips

**Issue**: Edge case candidate disqualified unexpectedly
- Check: Experience parsing (is "12 months" = 1 year?)
- Check: Threshold logic (>= vs >)

**Issue**: Wrong level assigned
- Check: Education substitution calculation
- Check: Job level thresholds match expected

**Issue**: Unexpected ranking
- Check: Scoring weights are default
- Check: Experience capping at 15 years
- Check: Skills capping at 10 points

---

## Test Data Statistics

**Total Files Created**: 12 PDFs (2 jobs + 10 resumes)
**Total Test Cases**: 10 candidates across 2 job types
**Edge Cases Covered**: 4 critical scenarios
**Test Time**: ~10 minutes for full validation

**Coverage**:
- ✅ Entry-level positions
- ✅ Multi-level positions (I-II, II-IV)
- ✅ Education requirements (HS Diploma, Bachelor's)
- ✅ Education substitution
- ✅ Exact threshold experience
- ✅ Missing required skills
- ✅ Insufficient experience
- ✅ Skills vs experience mismatches
