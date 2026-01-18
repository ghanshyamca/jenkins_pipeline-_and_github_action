# GitHub Actions CI/CD Pipeline

Complete CI/CD workflow for automated testing, building, and deployment of Flask application using GitHub Actions.

## 🎯 Overview

This GitHub Actions workflow automates the entire software delivery process:

```
Push Code → Test → Security Scan → Build → Deploy to Staging/Production → Notify
```

**Workflow File**: [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml)

**Workflow URL**: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

---

## ✨ Features

### 🔄 Continuous Integration
- ✅ Automated testing with pytest
- ✅ Code coverage reporting (88%+)
- ✅ Code quality checks (flake8)
- ✅ Security vulnerability scanning (Safety, Bandit)
- ✅ Python syntax validation

### 🚀 Continuous Deployment
- ✅ Automated deployment to staging (on `staging` branch)
- ✅ Automated deployment to production (on version tags)
- ✅ SSH-based deployment to EC2 instances
- ✅ Smoke tests and health checks
- ✅ Service restart automation

### 📦 Build & Artifacts
- ✅ Build artifact creation and storage
- ✅ Test results preservation
- ✅ Coverage reports (HTML & XML)
- ✅ Security scan reports
- ✅ 30-day artifact retention

### 📧 Notifications
- ✅ Email notifications on success
- ✅ Email notifications on failure
- ✅ Deployment status updates
- ✅ Detailed error reporting

---

## 🏗️ Workflow Architecture

```mermaid
graph TD
    A[Push Code] --> B[Test Job]
    B --> C[Security Scan Job]
    B --> D[Build Job]
    C --> D
    D --> E{Branch?}
    E -->|staging| F[Deploy to Staging]
    E -->|tag: v*| G[Deploy to Production]
    F --> H[Smoke Tests]
    G --> I[Health Checks]
    H --> J[Success Email]
    I --> K[Success Email + GitHub Release]
    B -.failure.-> L[Failure Email]
    C -.failure.-> L
    D -.failure.-> L
    F -.failure.-> L
    G -.failure.-> L
```

### Workflow Components

| Component | Purpose | Runs On |
|-----------|---------|---------|
| **Test** | Unit tests, coverage, linting | Every push/PR |
| **Security** | Vulnerability scanning | After tests pass |
| **Build** | Create deployment artifact | After tests & security |
| **Deploy Staging** | Deploy to staging server | Push to `staging` branch |
| **Deploy Production** | Deploy to production server | Push tag `v*` |
| **Notify** | Email notifications | Success/Failure |

---

## 📋 Prerequisites

### Required Accounts
- [x] GitHub account with repository
- [x] AWS account (for EC2 instances)
- [x] Email account (Gmail/SendGrid for notifications)

### Infrastructure Setup
- [x] **Staging EC2 instance** (t2.micro - free tier)
- [x] **Production EC2 instance** (t2.small recommended)
- [x] Both servers configured with Python, Nginx, and systemd service

### Repository Setup
- [x] Flask application in repository
- [x] Tests written (pytest)
- [x] `requirements.txt` with dependencies
- [x] Workflow file in `.github/workflows/ci-cd.yml`

---

## 🚀 Quick Start

### Step 1: Fork/Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### Step 2: Setup EC2 Servers

**Quick setup:**
```bash
# On both staging and production servers:
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv nginx
sudo mkdir -p /var/www/flask-app
sudo chown ubuntu:ubuntu /var/www/flask-app
cd /var/www/flask-app
python3 -m venv venv
```
<img width="1920" height="869" alt="image" src="https://github.com/user-attachments/assets/d158c4c1-0ee9-405f-819c-f288fa32dd94" />

<img width="1920" height="869" alt="image" src="https://github.com/user-attachments/assets/643f0dc5-2786-47f2-93b2-d73caddd56f7" />

### Step 3: Configure GitHub Secrets

Go to: **Repository → Settings → Secrets and variables → Actions**

Add these **14 secrets**:

📂 Deployment Secrets (8)

**Staging:**
```
STAGING_HOST         → 3.110.45.123 (your EC2 IP)
STAGING_USER         → ubuntu
STAGING_SSH_KEY      → [private SSH key content]
STAGING_DEPLOY_PATH  → /var/www/flask-app
```

**Production:**
```
PRODUCTION_HOST         → 13.234.56.78 (your EC2 IP)
PRODUCTION_USER         → ubuntu
PRODUCTION_SSH_KEY      → [private SSH key content]
PRODUCTION_DEPLOY_PATH  → /var/www/flask-app
```

**For Gmail:**
```
EMAIL_SERVER      → smtp.gmail.com
EMAIL_PORT        → 587
EMAIL_USERNAME    → yourproject.cicd@gmail.com
EMAIL_PASSWORD    → [Gmail App Password - 16 chars]
EMAIL_FROM        → yourproject.cicd@gmail.com
EMAIL_RECIPIENTS  → your.email@gmail.com
```

**Setup Gmail App Password:**
1. [Google Account](https://myaccount.google.com/) → Security
2. Enable 2-Step Verification
3. App passwords → Generate for "Mail"
4. Copy 16-character password

<img width="1920" height="1849" alt="image" src="https://github.com/user-attachments/assets/f30c14f0-ce87-4b59-bb2f-40a6540bc785" />

### Step 4: Push Code to Staging

```bash
# Initial setup
git add .
git commit -m "Setup GitHub Actions CI/CD"
git push origin staging
```

### Step 5: View Workflow

1. Go to **Actions** tab in GitHub
2. See workflow running in real-time
3. View logs for each job
4. Check email for notifications

---

<img width="1920" height="1521" alt="image" src="https://github.com/user-attachments/assets/baffd622-316d-4e3b-8a6b-d1463fed3afb" />

<img width="1515" height="558" alt="image" src="https://github.com/user-attachments/assets/a0180435-acb3-4d7f-9836-a6bc90910166" />



## 🔧 Workflow Jobs

### Job 1: Test Application

**Runs on**: `ubuntu-latest`  
**Triggers**: Every push, pull request  
**Duration**: ~2 minutes

```yaml
Steps:
1. Checkout code
2. Setup Python 3.9
3. Install dependencies
4. Lint with flake8
5. Run pytest tests
6. Generate coverage report
7. Upload test results
8. Upload coverage report
```

**Artifacts Created:**
- `test-results.xml` (JUnit format)
- `coverage-report/` (HTML coverage report)

**Success Criteria:**
- All tests pass (11/11)
- Coverage ≥ 88%
- No critical flake8 errors

### Job 2: Security Scan

**Runs on**: `ubuntu-latest`  
**Triggers**: After tests pass  
**Duration**: ~1 minute

```yaml
Steps:
1. Checkout code
2. Setup Python 3.9
3. Install dependencies
4. Run Safety check (dependency vulnerabilities)
5. Run Bandit scan (code security issues)
6. Upload security report
```

**Artifacts Created:**
- `bandit-report.json` (security scan results)

**Success Criteria:**
- No high-severity vulnerabilities
- No critical security issues

### Job 3: Build Application

**Runs on**: `ubuntu-latest`  
**Triggers**: After test & security pass  
**Duration**: ~1 minute

```yaml
Steps:
1. Checkout code
2. Setup Python 3.9
3. Install dependencies
4. Create build artifact (tar.gz)
5. Upload build artifact
```

**Artifacts Created:**
- `flask-app-<commit-sha>.tar.gz` (deployable package)
- Retained for 30 days

**Build Contents:**
```
build/
├── app.py
└── requirements.txt
```

### Job 4: Deploy to Staging

**Runs on**: `ubuntu-latest`  
**Triggers**: Push to `staging` branch  
**Duration**: ~2-3 minutes

```yaml
Steps:
1. Download build artifact
2. Setup SSH connection
3. Copy files to staging server (SCP)
4. Extract and install dependencies
5. Restart Flask service
6. Run smoke tests
7. Send success email
```

**Deployment Process:**
```bash
# On GitHub Actions runner:
scp flask-app.tar.gz ubuntu@staging-server:/var/www/flask-app/

# On staging server:
cd /var/www/flask-app
tar -xzf flask-app.tar.gz
cd build && ../venv/bin/pip install -r requirements.txt
cp build/* .
sudo systemctl restart flask-app
```

**Smoke Tests:**
- `curl http://staging-server/api/health` (must return 200)
- `curl http://staging-server/api/info` (must return 200)

**Success Criteria:**
- Files transferred successfully
- Dependencies installed
- Service restarted without errors
- Smoke tests pass

### Job 5: Deploy to Production

**Runs on**: `ubuntu-latest`  
**Triggers**: Push tag `v*` (e.g., v1.0.0)  
**Duration**: ~2-3 minutes

```yaml
Steps:
1. Download build artifact
2. Setup SSH connection
3. Copy files to production server (SCP)
4. Extract and install dependencies
5. Restart Flask service
6. Run health checks
7. Create GitHub Release
8. Send success email
```

**Health Checks:**
- `curl http://production-server/api/health`
- `curl http://production-server/api/info`

**GitHub Release:**
- Automatically created with tag
- Includes build artifact
- Release notes generated

**Success Criteria:**
- Zero-downtime deployment
- Health checks pass
- Service running properly

### Job 6: Notify on Failure

**Runs on**: `ubuntu-latest`  
**Triggers**: Any job failure  
**Duration**: ~30 seconds

```yaml
Steps:
1. Send failure email notification
```

**Email Includes:**
- Repository and branch
- Commit SHA and author
- Job that failed
- Link to workflow run logs

---

## ⚙️ Configuration

### Environment Variables

Defined at workflow level:

```yaml
env:
  PYTHON_VERSION: '3.9'
  FLASK_APP: app.py
```

### Workflow Triggers

```yaml
on:
  push:
    branches:
      - main        # Runs: test, security, build
      - staging     # Runs: test, security, build, deploy-staging
    tags:
      - 'v*'        # Runs: test, security, build, deploy-production
  pull_request:
    branches:
      - main        # Runs: test, security, build
      - staging
  workflow_dispatch:  # Manual trigger from GitHub UI
```

### Python Version

To change Python version, update workflow:

```yaml
env:
  PYTHON_VERSION: '3.11'  # Change to desired version
```

### Test Framework

Currently using pytest. To change:

```yaml
- name: Run Tests
  run: |
    # Replace pytest with your test framework
    python -m unittest discover
```

---

## 🚀 Deployment

### Deploy to Staging

```bash
# Create staging branch (first time)
git checkout -b staging

# Or switch to existing staging branch
git checkout staging

# Merge changes from main
git merge main

# Push to trigger deployment
git push origin staging
```

**What happens:**
1. ✅ Tests run
2. ✅ Security scan
3. ✅ Build artifact
4. ✅ Deploy to staging EC2
5. ✅ Smoke tests
6. ✅ Email notification

**Staging URL**: `http://STAGING_HOST` (from secrets)

### Deploy to Production

```bash
# Ensure main branch is ready
git checkout main

# Create version tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag to trigger production deployment
git push origin v1.0.0
```

**What happens:**
1. ✅ All tests run
2. ✅ Security scan
3. ✅ Build artifact
4. ✅ Deploy to production EC2
5. ✅ Health checks
6. ✅ GitHub Release created
7. ✅ Email notification

**Production URL**: `http://PRODUCTION_HOST` (from secrets)

### Version Tagging Best Practices

Follow Semantic Versioning (SemVer):

```bash
# Major release (breaking changes)
git tag -a v2.0.0 -m "Major release with breaking changes"

# Minor release (new features, backward compatible)
git tag -a v1.1.0 -m "Added new features"

# Patch release (bug fixes)
git tag -a v1.0.1 -m "Fixed bugs"

# Push tag
git push origin v1.0.1
```

### Rollback Production

```bash
# Deploy previous version
git tag -a v1.0.0-rollback -m "Rollback to v1.0.0"
git push origin v1.0.0-rollback

# Or re-push existing tag (force)
git push origin v1.0.0 --force
```

---

## 📧 Email Notifications

### Success Emails

**Staging Deployment Success:**
```
Subject: ✅ Staging Deployment Successful - Flask CI/CD

Staging Deployment Successful!

Repository: username/flask-app
Branch: staging
Commit: abc123def456
Author: yourusername

Staging URL: http://3.110.45.123

All smoke tests passed successfully.

View workflow run: https://github.com/.../actions/runs/123
```

**Production Deployment Success:**
```
Subject: ✅ Production Deployment Successful - Flask CI/CD

Production Deployment Successful!

Repository: username/flask-app
Tag: v1.0.0
Commit: abc123def456
Author: yourusername

Production URL: http://13.234.56.78

All health checks passed successfully.

View workflow run: https://github.com/.../actions/runs/123
```

### Failure Emails

```
Subject: ❌ CI/CD Pipeline Failed - Flask Application

CI/CD Pipeline Failed!

Repository: username/flask-app
Branch: main
Commit: abc123def456
Author: yourusername
Triggered by: push

⚠️ One or more jobs failed in the pipeline.

Please check the logs for details:
https://github.com/.../actions/runs/123

Failed at: 2026-01-18T10:30:00Z
```

### Configure Email Recipients

Multiple recipients (comma-separated):

```
EMAIL_RECIPIENTS: email1@example.com,email2@example.com,email3@example.com
```

See: [docs/EMAIL_NOTIFICATION_SETUP.md](docs/EMAIL_NOTIFICATION_SETUP.md)

---

## 🔐 Secrets Configuration

### Complete Secrets List

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `STAGING_HOST` | Staging server IP/domain | `3.110.45.123` |
| `STAGING_USER` | SSH username for staging | `ubuntu` |
| `STAGING_SSH_KEY` | Private SSH key for staging | `-----BEGIN RSA PRIVATE KEY-----...` |
| `STAGING_DEPLOY_PATH` | Deployment path on staging | `/var/www/flask-app` |
| `PRODUCTION_HOST` | Production server IP/domain | `13.234.56.78` |
| `PRODUCTION_USER` | SSH username for production | `ubuntu` |
| `PRODUCTION_SSH_KEY` | Private SSH key for production | `-----BEGIN RSA PRIVATE KEY-----...` |
| `PRODUCTION_DEPLOY_PATH` | Deployment path on production | `/var/www/flask-app` |
| `EMAIL_SERVER` | SMTP server address | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USERNAME` | SMTP username | `yourproject.cicd@gmail.com` |
| `EMAIL_PASSWORD` | SMTP password/API key | `abcd efgh ijkl mnop` |
| `EMAIL_FROM` | Sender email address | `yourproject.cicd@gmail.com` |
| `EMAIL_RECIPIENTS` | Recipient email addresses | `your.email@gmail.com` |

### How to Add Secrets

1. Go to GitHub repository
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter **Name** and **Value**
5. Click **Add secret**

### Security Best Practices

- ✅ Never commit secrets to repository
- ✅ Rotate SSH keys every 90 days
- ✅ Use separate SSH keys for staging and production
- ✅ Limit SSH key permissions on servers
- ✅ Use App Passwords instead of account passwords
- ✅ Monitor secret access in audit logs

---

## 📦 Artifacts

### Viewing Artifacts

1. Go to **Actions** tab
2. Click on a workflow run
3. Scroll to **Artifacts** section
4. Download artifacts

### Available Artifacts

| Artifact | Contents | Retention | Size |
|----------|----------|-----------|------|
| `test-results` | JUnit XML test results | 90 days | ~5 KB |
| `coverage-report` | HTML coverage report | 90 days | ~100 KB |
| `security-report` | Bandit JSON scan results | 90 days | ~10 KB |
| `flask-app-artifact` | Deployable tar.gz | 30 days | ~50 KB |

### Downloading Coverage Report

```bash
# Using GitHub CLI
gh run list
gh run download <run-id> -n coverage-report

# Manually
# 1. Go to Actions → Select run
# 2. Download "coverage-report" artifact
# 3. Extract and open htmlcov/index.html
```

---

## 🔍 Troubleshooting

### ❌ Tests Failing

**Check:**
```bash
# Run tests locally
python -m pytest test_app.py -v

# Check specific failing test
python -m pytest test_app.py::test_name -v
```

**Common issues:**
- Import errors → Check `requirements.txt`
- Environment variables → Add to workflow env
- Database connections → Use test database

### ❌ Build Artifact Upload Failed

**Error**: `No files found with the provided path`

**Solution:**
```yaml
# Verify build artifact exists
- name: Create Build Artifact
  run: |
    mkdir -p build
    cp app.py build/
    cp requirements.txt build/
    ls -la build/  # Verify files
    tar -czf flask-app-${{ github.sha }}.tar.gz build/
    ls -la flask-app-*.tar.gz  # Verify archive
```

### ❌ SSH Deployment Failed

**Error**: `Permission denied (publickey)`

**Check:**
1. SSH key added to server's `~/.ssh/authorized_keys`
2. Private key correctly pasted in GitHub Secret
3. No extra spaces or newlines in secret
4. Correct username (ubuntu, ec2-user, etc.)

**Test SSH connection:**
```bash
# On local machine
ssh -i ~/.ssh/github_actions_staging ubuntu@STAGING_HOST
```

### ❌ Service Restart Failed

**Error**: `Failed to restart flask-app.service`

**Check on server:**
```bash
# Check service status
sudo systemctl status flask-app

# Check logs
sudo journalctl -u flask-app -n 50

# Verify systemd file
cat /etc/systemd/system/flask-app.service

# Manually restart
sudo systemctl restart flask-app
```

### ❌ Email Not Received

**Check:**
1. All 6 email secrets configured correctly
2. Check spam/junk folder
3. Verify email in workflow logs
4. Gmail: Use App Password, not account password
5. SendGrid: Verify sender email

**Test email locally:**
```python
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your.email@gmail.com', 'app-password')
server.sendmail('from@gmail.com', 'to@gmail.com', 'Subject: Test\n\nBody')
server.quit()
```

### ❌ Workflow Not Triggering

**Check:**
1. Workflow file in `.github/workflows/ci-cd.yml`
2. Valid YAML syntax (use YAML validator)
3. Branch name matches trigger configuration
4. Tag format matches pattern (v*)

**Enable workflow:**
```
Repository → Actions → Select workflow → Enable workflow
```

### ❌ Artifact Download Failed

**Error**: `Unable to find artifact`

**Solution:**
- Artifacts only available after upload step completes
- Check if previous job succeeded
- Verify artifact name matches exactly

---

## 📊 Workflow Metrics

### Typical Execution Times

| Job | Duration | Notes |
|-----|----------|-------|
| Test | 1-2 min | Depends on test count |
| Security | 30-60 sec | Scanning dependencies |
| Build | 30-60 sec | Creating artifact |
| Deploy Staging | 2-3 min | Includes smoke tests |
| Deploy Production | 2-3 min | Includes health checks |
| **Total** | **5-10 min** | Full pipeline |

### GitHub Actions Limits

**Free tier (Public repos):**
- ✅ Unlimited minutes
- ✅ Unlimited storage

**Free tier (Private repos):**
- ⚠️ 2,000 minutes/month
- ⚠️ 500 MB storage

**Paid plans:**
- See [GitHub Pricing](https://github.com/pricing)

---

## 🎓 Best Practices

### 1. Branch Strategy

```
main       → Production-ready code
staging    → Pre-production testing
feature/*  → New features (PR to main)
hotfix/*   → Urgent fixes (PR to main)
```

### 2. Version Tagging

```bash
# Semantic Versioning: MAJOR.MINOR.PATCH
v1.0.0  → Initial release
v1.0.1  → Bug fix
v1.1.0  → New feature
v2.0.0  → Breaking change
```

### 3. Deployment Workflow

```
1. Develop → feature branch
2. Test → create PR to main
3. Review → code review
4. Merge → to main (runs tests)
5. Deploy Staging → merge main to staging
6. QA Testing → test on staging
7. Deploy Production → tag release
8. Monitor → check logs and metrics
```

### 4. Rollback Strategy

```bash
# Quick rollback
git tag -a v1.0.0-rollback -m "Rollback to v1.0.0"
git push origin v1.0.0-rollback

# Or manual SSH deployment
ssh ubuntu@production-server
cd /var/www/flask-app
git checkout v1.0.0  # If using git
sudo systemctl restart flask-app
```

### 5. Monitoring

- ✅ Enable GitHub email notifications
- ✅ Monitor workflow runs regularly
- ✅ Check server logs after deployment
- ✅ Set up uptime monitoring (UptimeRobot, Pingdom)
- ✅ Review security scan reports

---

## 📚 Additional Resources

### Documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [AWS EC2 Setup Guide](docs/AWS_EC2_SETUP.md)
- [Email Notification Setup](docs/EMAIL_NOTIFICATION_SETUP.md)

### Related Files
- [Workflow File](.github/workflows/ci-cd.yml)
- [Flask Application](app.py)
- [Tests](test_app.py)
- [Requirements](requirements.txt)

### Support
- GitHub Issues: [Create Issue](../../issues)
- Discussions: [GitHub Discussions](../../discussions)

---

## ✅ Quick Reference

### Common Commands

```bash
# Run tests locally
pytest test_app.py -v --cov=app

# Deploy to staging
git checkout staging
git merge main
git push origin staging

# Deploy to production
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# View workflow runs
gh run list
gh run view <run-id>

# Download artifacts
gh run download <run-id>
```

### Workflow Status Badge

Add to README.md:

```markdown
![CI/CD Pipeline](https://github.com/USERNAME/REPO/actions/workflows/ci-cd.yml/badge.svg)
```

### Useful Links

- **Actions Tab**: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
- **Workflow File**: `https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/.github/workflows/ci-cd.yml`
- **Secrets**: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`

---

**🚀 Your GitHub Actions CI/CD pipeline is ready!**

Push to `main` for testing, `staging` for staging deployment, or create a tag for production deployment. Happy deploying! 🎉
