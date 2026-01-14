#!/usr/bin/env python3
"""
Pre-Deployment Check Script
============================
Run this before deploying to Streamlit Cloud to verify all dependencies and files are ready.

Usage:
    python3 pre_deployment_check.py
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version is 3.8+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor}.{version.micro} is too old. Need 3.8+")
        return False

def check_required_files():
    """Check that all required files exist"""
    required_files = [
        "streamlit_app.py",
        "utils.py",
        "requirements.txt",
        ".streamlit/config.toml",
        ".gitignore",
        "README.md",
        "sample_data/generated/ActualJobs/TxDOT Data Analyst 1-5.pdf",
        "sample_data/generated/DemoResumes"
    ]

    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_exist = False

    return all_exist

def check_demo_resumes():
    """Check that demo resumes exist"""
    demo_dir = Path("sample_data/generated/DemoResumes")
    if not demo_dir.exists():
        print("❌ Demo resumes directory not found")
        return False

    pdf_files = list(demo_dir.glob("*.pdf"))
    if len(pdf_files) >= 5:
        print(f"✅ Demo resumes: {len(pdf_files)} PDFs found")
        return True
    else:
        print(f"❌ Demo resumes: Only {len(pdf_files)} PDFs found (need at least 5)")
        return False

def check_dependencies():
    """Check that all required packages are importable"""
    packages = {
        "streamlit": "Streamlit",
        "pypdf": "PyPDF",
        "pandas": "Pandas",
        "reportlab": "ReportLab"
    }

    all_installed = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name} installed")
        except ImportError:
            print(f"❌ {name} not installed (pip install {package})")
            all_installed = False

    return all_installed

def check_no_secrets():
    """Check that no secrets.toml exists (should not be committed)"""
    secrets_path = Path(".streamlit/secrets.toml")
    if secrets_path.exists():
        print("⚠️  WARNING: .streamlit/secrets.toml exists. This should NOT be committed to git!")
        print("   Make sure it's in .gitignore")
        return False
    else:
        print("✅ No secrets.toml file (good - no API keys needed)")
        return True

def check_gitignore():
    """Check that .gitignore has essential entries"""
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        print("❌ .gitignore does not exist")
        return False

    content = gitignore_path.read_text()
    required_patterns = [
        ("__pycache__", "__pycache__"),
        ("*.pyc or *.py[cod]", ["*.pyc", "*.py[cod]"]),
        (".streamlit/secrets.toml", ".streamlit/secrets.toml")
    ]

    all_present = True
    for description, patterns in required_patterns:
        if isinstance(patterns, list):
            # Check if any of the patterns match
            found = any(p in content for p in patterns)
        else:
            found = patterns in content

        if found:
            print(f"✅ .gitignore contains: {description}")
        else:
            print(f"❌ .gitignore missing: {description}")
            all_present = False

    return all_present

def check_no_openai_references():
    """Check that OpenAI integration has been removed"""
    files_to_check = ["streamlit_app.py", "utils.py", "requirements.txt"]

    found_references = []
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            content = path.read_text()
            if "openai" in content.lower() or "OPENAI_API_KEY" in content:
                found_references.append(file_path)

    if found_references:
        print(f"❌ OpenAI references found in: {', '.join(found_references)}")
        return False
    else:
        print("✅ No OpenAI references found (integration successfully removed)")
        return True

def main():
    """Run all checks"""
    print("=" * 60)
    print("CandidateCompass - Pre-Deployment Check")
    print("=" * 60)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Demo Resumes", check_demo_resumes),
        ("Dependencies", check_dependencies),
        ("No Secrets File", check_no_secrets),
        (".gitignore Configuration", check_gitignore),
        ("OpenAI Integration Removed", check_no_openai_references)
    ]

    results = []
    for check_name, check_func in checks:
        print(f"\n--- {check_name} ---")
        result = check_func()
        results.append((check_name, result))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")

    print(f"\nTotal: {passed}/{total} checks passed")

    if passed == total:
        print("\n🎉 All checks passed! Your app is ready for deployment.")
        print("\nNext steps:")
        print("1. git init && git add . && git commit -m 'Initial commit'")
        print("2. Create GitHub repo and push code")
        print("3. Deploy to Streamlit Cloud at https://share.streamlit.io")
        print("\nSee DEPLOYMENT_GUIDE.md for detailed instructions.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please fix the issues above before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
