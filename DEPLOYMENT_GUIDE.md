# CandidateCompass - Streamlit Cloud Deployment Guide

## Pre-Deployment Checklist

### ✅ Prerequisites Completed
- [x] OpenAI integration removed from code
- [x] `requirements.txt` updated (removed OpenAI dependency)
- [x] `.gitignore` file created
- [x] `.streamlit/config.toml` configured with CGI branding
- [x] Demo data present (`sample_data/generated/DemoResumes/` - 8 PDFs)
- [x] Job description present (`sample_data/generated/ActualJobs/TxDOT Data Analyst 1-5.pdf`)
- [x] Documentation complete (README.md, PRODUCT_OVERVIEW.md, etc.)

### 📦 What Will Be Deployed
- **Application size**: ~8MB (including sample PDFs)
- **Python version**: 3.8+ (Streamlit Cloud will use Python 3.11 by default)
- **Dependencies**: Streamlit, pypdf, pandas, reportlab (no API keys needed)
- **Demo data**: 8 candidate resumes + 1 job description

---

## Deployment Steps

### Step 1: Initialize Git Repository (If Not Already Done)

```bash
# Navigate to project directory
cd /Users/alexiandrea/streamlit-candidate-ranker

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: CandidateCompass demo app"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Repository settings:
   - **Name**: `candidate-compass` (or your preferred name)
   - **Description**: "AI-assisted resume screening demo for government hiring workshops"
   - **Visibility**:
     - **Public** (recommended for demo/portfolio)
     - **Private** (if confidential)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

### Step 3: Push Code to GitHub

```bash
# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/candidate-compass.git

# Push code
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Configure deployment:
   - **Repository**: Select your GitHub repo (`YOUR_USERNAME/candidate-compass`)
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Choose your custom subdomain (e.g., `candidate-compass.streamlit.app`)
4. Click **"Deploy!"**

### Step 5: Wait for Deployment

- Initial deployment takes 2-5 minutes
- Streamlit Cloud will:
  - Install Python dependencies from `requirements.txt`
  - Apply theme from `.streamlit/config.toml`
  - Start the application
- Monitor progress in the deployment logs

### Step 6: Test Your Deployed App

Once deployed, test these critical features:

1. **Launch Demo button** - Loads 8 candidates + job description
2. **Scoring rubric** - Adjust sliders and verify rankings update
3. **Candidate details** - Expand top candidates, check scores
4. **Interview questions** - Verify template questions generate correctly
5. **Downloads** - Test CSV export and PDF generation
6. **Mobile view** - Check responsiveness on phone/tablet

---

## Post-Deployment Configuration

### Streamlit Cloud Settings

1. Go to your app dashboard on [share.streamlit.io](https://share.streamlit.io)
2. Click on your app → **Settings** (⚙️ icon)
3. Recommended settings:
   - **Python version**: 3.11 (default)
   - **Resources**: Default (0.5 GB memory, 1 CPU core)
   - **Secrets**: None needed (OpenAI integration removed)

### Custom Domain (Optional)

If you want a custom domain (e.g., `candidatecompass.yourcompany.com`):

1. In app Settings → **General**
2. Scroll to **Custom subdomain**
3. Follow instructions to configure DNS CNAME record

---

## Updating Your Deployed App

After making changes to your code:

```bash
# Make your changes locally
# Test locally: streamlit run streamlit_app.py

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

Streamlit Cloud will automatically detect the push and redeploy (takes ~1-2 minutes).

---

## Troubleshooting

### Issue: App won't start or shows import errors

**Solution**: Check the deployment logs for missing dependencies
- Verify `requirements.txt` has all necessary packages
- Ensure version numbers are compatible

### Issue: Demo data not loading

**Solution**: Verify file paths
- Check that `sample_data/generated/DemoResumes/` exists in GitHub
- Ensure PDFs are committed (not in `.gitignore`)
- Verify file paths use forward slashes (`/`) not backslashes

### Issue: Theme colors not applying

**Solution**: Check `.streamlit/config.toml`
- Ensure it's committed to GitHub
- Verify TOML syntax is correct
- Clear browser cache and refresh

### Issue: App runs locally but fails on Streamlit Cloud

**Solution**: Check Python version compatibility
- Test with Python 3.11 locally: `pyenv install 3.11 && pyenv local 3.11`
- Ensure no hardcoded file paths (use `Path` from `pathlib`)
- Check for OS-specific code (e.g., Windows-only libraries)

---

## Resource Limits

Streamlit Community Cloud (free tier) has these limits:

- **Memory**: 1 GB RAM
- **CPU**: 1 CPU core
- **Storage**: 1 GB (for your app + dependencies)
- **Concurrent users**: Recommended ~10-20 simultaneous users
- **Sleep policy**: Apps sleep after 7 days of inactivity (wake on visit)

Your app should easily fit within these limits.

---

## Security Notes

### ✅ Security Best Practices Applied

- No API keys required (OpenAI integration removed)
- No `.streamlit/secrets.toml` needed
- All demo data is fictional and anonymized
- No real PII is processed or stored
- No persistent database (session-only storage)
- `.gitignore` prevents accidental secret commits

### ⚠️ Demo Disclaimer

This is a **demonstration tool** for workshops, not a production hiring system. The deployed app should include:

- Clear "DEMO ONLY" banners (already present)
- Disclaimer about fictional data (already present)
- Warning that real hiring decisions require human review (already present)

---

## Monitoring & Analytics

### Built-in Streamlit Metrics

Streamlit Cloud provides basic analytics:
- **Views**: Number of sessions
- **Active time**: Total usage time
- **Last active**: Most recent access

Access via app dashboard → **Analytics** tab

### Usage Stats

The app currently has `gatherUsageStats = false` in config.toml to respect privacy. Change to `true` if you want Streamlit to collect anonymous usage data.

---

## Sharing Your App

Once deployed, share your app URL:

```
https://YOUR-SUBDOMAIN.streamlit.app
```

**Recommended sharing contexts:**
- Workshop registration emails
- Training session links
- Demo during presentations (screenshare the live app)
- Portfolio/resume projects section
- LinkedIn posts about your work

**Include this description:**
> "CandidateCompass: An interactive demo showcasing AI-assisted resume screening for government hiring. Features qualification gating, multi-level position matching, and responsible AI guardrails. Try the live demo!"

---

## Cost

**Streamlit Community Cloud**: 100% FREE
- No credit card required
- Unlimited public apps
- Automatic SSL/HTTPS
- Continuous deployment from GitHub

**Streamlit for Teams** (optional upgrade):
- Private apps
- Password protection
- More resources
- Priority support
- Starts at $250/month (not needed for your demo)

---

## Next Steps After Deployment

### For Workshops

1. **Test the live URL** - Verify all features work
2. **Bookmark the URL** - Add to browser favorites
3. **Screen share the live app** - During presentations
4. **Share with participants** - Send URL in advance or during session

### For Portfolio/Resume

1. **Add to LinkedIn** - Projects section
2. **Add to resume** - Include live demo URL
3. **Write a blog post** - Explain design decisions and responsible AI features
4. **Create a video walkthrough** - Screen recording with narration

### For Further Development

1. **Collect user feedback** - Add feedback form link
2. **Track metrics** - Monitor usage patterns
3. **Iterate on features** - Based on workshop feedback
4. **Expand test data** - Add more sample job descriptions

---

## Support Resources

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Streamlit Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Streamlit Cloud Status**: [status.streamlit.io](https://status.streamlit.io)
- **GitHub Issues**: Report bugs in your repo

---

## Deployment Summary

**Ready to deploy?** ✅

Your app is fully prepared for Streamlit Cloud deployment. All prerequisites are met:

- ✅ Code is clean and tested
- ✅ Dependencies are documented
- ✅ Demo data is included
- ✅ Configuration is complete
- ✅ Documentation is comprehensive
- ✅ No secrets or API keys required

**Estimated time to deploy**: 15-20 minutes (including GitHub setup)

**Command sequence**:
```bash
git init
git add .
git commit -m "Initial commit: CandidateCompass demo app"
git remote add origin https://github.com/YOUR_USERNAME/candidate-compass.git
git push -u origin main
```

Then go to [share.streamlit.io](https://share.streamlit.io) and click "New app"!

---

**Questions?** Review the troubleshooting section above or check the Streamlit documentation.

**Good luck with your deployment! 🚀**
