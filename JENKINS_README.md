# Jenkins CI/CD Pipeline

Complete CI/CD pipeline for automated testing, building, and deployment of Flask application using Jenkins.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Pipeline Architecture](#pipeline-architecture)
- [Prerequisites](#prerequisites)
- [Jenkins Setup](#jenkins-setup)
- [Pipeline Stages](#pipeline-stages)
- [Configuration](#configuration)
- [Credentials Setup](#credentials-setup)
- [Running the Pipeline](#running-the-pipeline)
- [Email Notifications](#email-notifications)
- [Troubleshooting](#troubleshooting)
- [Comparison with GitHub Actions](#comparison-with-github-actions)

---

## 🎯 Overview

This Jenkins pipeline automates the entire CI/CD process for the Flask application:

```
Git Push → Checkout → Setup → Build → Quality Check → Test → Security Scan → Deploy → Smoke Test → Notify
```

**Pipeline File**: [`Jenkinsfile`](Jenkinsfile)

**Jenkins URL**: `http://your-jenkins-server:8080`

---

## ✨ Features

### 🔄 Continuous Integration
- ✅ Automated source code checkout
- ✅ Python virtual environment setup
- ✅ Dependency installation
- ✅ Code quality checks (flake8)
- ✅ Unit testing with pytest
- ✅ Code coverage reporting (88%+)
- ✅ Security vulnerability scanning (Safety, Bandit)

### 🚀 Continuous Deployment
- ✅ Automated deployment to staging (on `staging` branch)
- ✅ Automated deployment to production (on version tags `v*`)
- ✅ SSH-based deployment to EC2 instances
- ✅ Smoke tests and health checks
- ✅ Service restart automation

### 📦 Build & Artifacts
- ✅ Build artifact creation (.tar.gz)
- ✅ Test results preservation (JUnit XML)
- ✅ Coverage reports (HTML)
- ✅ Security scan reports (JSON)
- ✅ Artifact archival and fingerprinting

### 📧 Notifications
- ✅ HTML email notifications on success
- ✅ HTML email notifications on failure
- ✅ Build status in email body
- ✅ Direct links to build console

---

## 🏗️ Pipeline Architecture

```
┌─────────────┐
│   Checkout  │ Git checkout
└──────┬──────┘
       │
┌──────▼──────┐
│Setup Environment│ Python venv
└──────┬──────┘
       │
┌──────▼──────┐
│    Build    │ Install dependencies
└──────┬──────┘
       │
┌──────▼──────┐
│Code Quality │ flake8 linting
└──────┬──────┘
       │
┌──────▼──────┐
│    Test     │ pytest + coverage
└──────┬──────┘
       │
┌──────▼──────┐
│Security Scan│ Safety + Bandit
└──────┬──────┘
       │
┌──────▼──────┐
│Build Artifact│ Create .tar.gz
└──────┬──────┘
       │
       ├─────────────────┬─────────────────┐
       │                 │                 │
┌──────▼──────┐   ┌─────▼─────┐   ┌──────▼──────┐
│Deploy Staging│   │Deploy Prod│   │   Skip      │
│(staging branch)│ │(tag v*)   │   │(other branches)│
└──────┬──────┘   └─────┬─────┘   └─────────────┘
       │                 │
┌──────▼──────┐   ┌─────▼─────┐
│Smoke Test   │   │Health Check│
└──────┬──────┘   └─────┬─────┘
       │                 │
       └────────┬────────┘
                │
         ┌──────▼──────┐
         │Email Notify │
         └─────────────┘
```

### Pipeline Stages

| Stage | Purpose | Runs On | Duration |
|-------|---------|---------|----------|
| **Checkout** | Clone repository | All branches | ~10s |
| **Setup Environment** | Create Python venv | All branches | ~30s |
| **Build** | Install dependencies | All branches | ~1-2 min |
| **Code Quality Check** | Run flake8 linting | All branches | ~15s |
| **Test** | Run pytest + coverage | All branches | ~1-2 min |
| **Security Scan** | Safety + Bandit scan | All branches | ~1 min |
| **Build Artifact** | Create deployment package | All branches | ~15s |
| **Deploy to Staging** | SSH deploy to staging | `staging` branch | ~2-3 min |
| **Deploy to Production** | SSH deploy to production | Tags `v*` | ~2-3 min |
| **Smoke Test** | Verify staging deployment | `staging` branch | ~10s |
| **Health Check** | Verify production deployment | Tags `v*` | ~10s |

**Total Duration**: 8-12 minutes (depending on stage execution)

---

## 📋 Prerequisites

### Required Software

#### On Jenkins Server:
- [x] **Jenkins 2.400+** installed and running
- [x] **Java 11 or 17** (required by Jenkins)
- [x] **Git** (for source code checkout)
- [x] **Python 3.9+** (for building and testing)
- [x] **SSH client** (for deployment)

#### On Target Servers (Staging/Production):
- [x] **Ubuntu 22.04 LTS** (or compatible Linux)
- [x] **Python 3.9+** with pip and venv
- [x] **Nginx** (reverse proxy)
- [x] **systemd** (for service management)
- [x] Flask app configured as systemd service

### Required Jenkins Plugins

Install these plugins from **Manage Jenkins → Plugin Manager**:

1. **Pipeline** (Pipeline plugin)
2. **Git** (Git plugin)
3. **Credentials Binding** (Credentials Binding Plugin)
4. **Email Extension** (Email Extension Plugin)
5. **JUnit** (JUnit Plugin)
6. **HTML Publisher** (HTML Publisher plugin)
7. **Workspace Cleanup** (Workspace Cleanup Plugin)

### Infrastructure

- **Staging EC2 Instance**: t2.micro (free tier eligible)
- **Production EC2 Instance**: t2.small or larger
- **SSH Access**: Both servers accessible from Jenkins

---

## 🚀 Jenkins Setup

### Step 1: Install Jenkins

**On Ubuntu 22.04:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Java 17
sudo apt install -y openjdk-17-jdk

# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt update
sudo apt install -y jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

**Access Jenkins**: `http://your-server-ip:8080`

### Step 2: Initial Configuration

1. **Unlock Jenkins**: Enter the initial admin password
2. **Install Plugins**: Select "Install suggested plugins"
3. **Create Admin User**: Set username and password
4. **Configure Jenkins URL**: `http://your-jenkins-server:8080`

### Step 3: Install Required Plugins

1. Go to **Manage Jenkins** → **Plugin Manager**
2. Click **Available plugins** tab
3. Search and install:
   - Pipeline
   - Git
   - Credentials Binding
   - Email Extension Plugin
   - HTML Publisher
   - JUnit Plugin

4. Click **Install without restart**
5. Restart Jenkins after installation

### Step 4: Configure System Tools

**Manage Jenkins → Tools**

#### Git Configuration:
- Name: `Default`
- Path to Git executable: `git` (or `/usr/bin/git`)

#### Python:
Jenkins will use system Python. Verify:
```bash
python3 --version  # Should be 3.9+
```

### Step 5: Configure Email

**Manage Jenkins → System → Extended E-mail Notification**

**For Gmail:**
- SMTP server: `smtp.gmail.com`
- SMTP port: `587`
- Use SSL: ✓
- Credentials: Add Gmail credentials (username + App Password)
- Default user e-mail suffix: `@gmail.com`

**Test configuration**: Click "Test configuration by sending test e-mail"

See: [docs/EMAIL_NOTIFICATION_SETUP.md](docs/EMAIL_NOTIFICATION_SETUP.md)

---

## ⚙️ Configuration

### Environment Variables (in Jenkinsfile)

```groovy
environment {
    PYTHON_VERSION = '3.9'              // Python version to use
    VIRTUAL_ENV = 'venv'                // Virtual environment name
    FLASK_APP = 'app.py'                // Flask application file
    
    // Deployment paths
    STAGING_DEPLOY_PATH = '/var/www/flask-app'
    PRODUCTION_DEPLOY_PATH = '/var/www/flask-app'
    
    // Email configuration
    EMAIL_RECIPIENTS = 'your-email@example.com'  // Update this!
}
```

### Branch-Based Deployment

```groovy
// Staging deployment - triggered by 'staging' branch
stage('Deploy to Staging') {
    when {
        branch 'staging'
    }
    // Deployment steps...
}

// Production deployment - triggered by tags matching v*.*.* pattern
stage('Deploy to Production') {
    when {
        tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
    }
    // Deployment steps...
}
```

---

## 🔐 Credentials Setup

### Add Credentials in Jenkins

**Manage Jenkins → Credentials → System → Global credentials → Add Credentials**

Add the following **10 credentials**:

#### 1. Staging Host
- **Kind**: Secret text
- **Scope**: Global
- **Secret**: `3.110.45.123` (your staging server IP)
- **ID**: `staging-host`
- **Description**: Staging Server IP/Hostname

#### 2. Staging User
- **Kind**: Secret text
- **Secret**: `ubuntu`
- **ID**: `staging-user`
- **Description**: Staging SSH Username

#### 3. Staging SSH Key
- **Kind**: Secret text
- **Secret**: [Paste entire private key content]
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```
- **ID**: `staging-ssh-key`
- **Description**: Staging SSH Private Key

#### 4. Production Host
- **Kind**: Secret text
- **Secret**: `13.234.56.78` (your production server IP)
- **ID**: `production-host`
- **Description**: Production Server IP/Hostname

#### 5. Production User
- **Kind**: Secret text
- **Secret**: `ubuntu`
- **ID**: `production-user`
- **Description**: Production SSH Username

#### 6. Production SSH Key
- **Kind**: Secret text
- **Secret**: [Paste entire private key content]
- **ID**: `production-ssh-key`
- **Description**: Production SSH Private Key

### Generate SSH Keys for Deployment

**On your local machine or Jenkins server:**

```bash
# Generate SSH key for staging
ssh-keygen -t rsa -b 4096 -f ~/.ssh/jenkins_staging -N ""

# Generate SSH key for production
ssh-keygen -t rsa -b 4096 -f ~/.ssh/jenkins_production -N ""

# Display public keys (add to servers)
cat ~/.ssh/jenkins_staging.pub
cat ~/.ssh/jenkins_production.pub

# Display private keys (add to Jenkins credentials)
cat ~/.ssh/jenkins_staging
cat ~/.ssh/jenkins_production
```

**Add public keys to servers:**

```bash
# SSH to staging server
ssh -i your-ec2-key.pem ubuntu@<STAGING-IP>

# Add Jenkins public key
echo "paste-public-key-here" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Repeat for production server
```

### Credentials Summary

| ID | Type | Description | Example Value |
|----|------|-------------|---------------|
| `staging-host` | Secret text | Staging server IP | `3.110.45.123` |
| `staging-user` | Secret text | Staging SSH user | `ubuntu` |
| `staging-ssh-key` | Secret text | Staging SSH private key | `-----BEGIN RSA...` |
| `production-host` | Secret text | Production server IP | `13.234.56.78` |
| `production-user` | Secret text | Production SSH user | `ubuntu` |
| `production-ssh-key` | Secret text | Production SSH private key | `-----BEGIN RSA...` |

---

## 🔧 Pipeline Stages

### Stage 1: Checkout

**Purpose**: Clone the Git repository

```groovy
stage('Checkout') {
    steps {
        echo 'Checking out source code...'
        checkout scm
    }
}
```

**What happens:**
- Clones repository from Git
- Uses branch/tag that triggered the build
- Checks out to Jenkins workspace

### Stage 2: Setup Environment

**Purpose**: Create Python virtual environment

```groovy
stage('Setup Environment') {
    steps {
        script {
            sh '''
                python3 -m venv ${VIRTUAL_ENV}
                . ${VIRTUAL_ENV}/bin/activate
                pip install --upgrade pip
            '''
        }
    }
}
```

**What happens:**
- Creates isolated Python environment
- Upgrades pip to latest version
- Prepares for dependency installation

### Stage 3: Build

**Purpose**: Install application dependencies

```groovy
stage('Build') {
    steps {
        script {
            sh '''
                . ${VIRTUAL_ENV}/bin/activate
                pip install -r requirements.txt
            '''
        }
    }
}
```

**What happens:**
- Activates virtual environment
- Installs all packages from requirements.txt
- Verifies successful installation

### Stage 4: Code Quality Check

**Purpose**: Run code linting with flake8

```groovy
stage('Code Quality Check') {
    steps {
        script {
            sh '''
                . ${VIRTUAL_ENV}/bin/activate
                flake8 app.py --max-line-length=120 --exclude=${VIRTUAL_ENV} || true
            '''
        }
    }
}
```

**What happens:**
- Checks code style and quality
- Identifies syntax errors
- Reports violations
- Continues even if violations found (|| true)

### Stage 5: Test

**Purpose**: Run unit tests with coverage

```groovy
stage('Test') {
    steps {
        script {
            sh '''
                . ${VIRTUAL_ENV}/bin/activate
                pytest test_app.py -v --junitxml=test-results.xml \
                       --cov=app --cov-report=xml --cov-report=html
            '''
        }
    }
    post {
        always {
            junit 'test-results.xml'
            publishHTML(target: [
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
    }
}
```

**What happens:**
- Runs all tests in test_app.py
- Generates JUnit XML results
- Creates coverage report (XML and HTML)
- Publishes results to Jenkins UI
- Coverage report viewable in build page

**Artifacts Created:**
- `test-results.xml` (JUnit format)
- `htmlcov/` (HTML coverage report)

### Stage 6: Security Scan

**Purpose**: Scan for security vulnerabilities

```groovy
stage('Security Scan') {
    steps {
        script {
            sh '''
                . ${VIRTUAL_ENV}/bin/activate
                pip install safety bandit
                
                # Check dependency vulnerabilities
                safety check --json > safety-report.json || true
                
                # Check code security issues
                bandit -r app.py -f json -o bandit-report.json || true
            '''
        }
    }
    post {
        always {
            archiveArtifacts artifacts: '*-report.json', allowEmptyArchive: true
        }
    }
}
```

**What happens:**
- **Safety**: Scans requirements.txt for vulnerable packages
- **Bandit**: Scans Python code for security issues
- Generates JSON reports
- Archives reports as build artifacts

**Artifacts Created:**
- `safety-report.json`
- `bandit-report.json`

### Stage 7: Build Artifact

**Purpose**: Create deployment package

```groovy
stage('Build Artifact') {
    steps {
        script {
            sh '''
                tar -czf flask-app-${BUILD_NUMBER}.tar.gz \
                    app.py requirements.txt \
                    --exclude=${VIRTUAL_ENV} \
                    --exclude=*.pyc \
                    --exclude=__pycache__
            '''
        }
        archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
    }
}
```

**What happens:**
- Creates compressed archive (.tar.gz)
- Includes app.py and requirements.txt
- Excludes virtual environment and Python cache
- Names file with build number
- Archives for download

**Artifact**: `flask-app-<build-number>.tar.gz`

### Stage 8: Deploy to Staging

**Purpose**: Deploy to staging server (only on `staging` branch)

**Trigger**: Push to `staging` branch

```groovy
stage('Deploy to Staging') {
    when {
        branch 'staging'
    }
    steps {
        script {
            sh '''
                # Setup SSH key
                mkdir -p ~/.ssh
                echo "${STAGING_SSH_KEY}" > ~/.ssh/deploy_key_staging
                chmod 600 ~/.ssh/deploy_key_staging
                
                # Copy files to server
                scp -i ~/.ssh/deploy_key_staging -o StrictHostKeyChecking=no \
                    flask-app-${BUILD_NUMBER}.tar.gz \
                    ${STAGING_USER}@${STAGING_HOST}:${STAGING_DEPLOY_PATH}
                
                # Extract and install
                ssh -i ~/.ssh/deploy_key_staging -o StrictHostKeyChecking=no \
                    ${STAGING_USER}@${STAGING_HOST} \
                    "cd ${STAGING_DEPLOY_PATH} && tar -xzf flask-app-${BUILD_NUMBER}.tar.gz"
                
                # Install dependencies
                ssh ... "cd ${STAGING_DEPLOY_PATH}/build && ../venv/bin/pip install -r requirements.txt"
                
                # Copy files and restart service
                ssh ... "cp ${STAGING_DEPLOY_PATH}/build/* ${STAGING_DEPLOY_PATH}/"
                ssh ... "sudo systemctl restart flask-app"
                
                # Cleanup
                rm -f ~/.ssh/deploy_key_staging
            '''
        }
    }
}
```

**What happens:**
1. Creates SSH key file from credentials
2. Copies artifact to staging server via SCP
3. Extracts files on server
4. Installs dependencies in server's venv
5. Copies files to deployment directory
6. Restarts Flask systemd service
7. Cleans up SSH key

### Stage 9: Deploy to Production

**Purpose**: Deploy to production server (only on version tags)

**Trigger**: Push tag matching `v*.*.*` (e.g., v1.0.0)

```groovy
stage('Deploy to Production') {
    when {
        tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
    }
    // Same steps as staging but using production credentials
}
```

**What happens:**
- Same deployment process as staging
- Uses production server credentials
- Only triggered by version tags
- More cautious deployment (production environment)

### Stage 10: Smoke Test (Staging)

**Purpose**: Verify staging deployment

```groovy
stage('Smoke Test - Staging') {
    when {
        branch 'staging'
    }
    steps {
        script {
            sh '''
                sleep 5  # Wait for service to start
                curl -f http://${STAGING_HOST}/api/health || exit 1
                curl -f http://${STAGING_HOST}/api/info || exit 1
            '''
        }
    }
}
```

**What happens:**
- Waits 5 seconds for service to stabilize
- Tests `/api/health` endpoint
- Tests `/api/info` endpoint
- Fails build if any endpoint fails

### Stage 11: Health Check (Production)

**Purpose**: Verify production deployment

```groovy
stage('Health Check - Production') {
    when {
        tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
    }
    // Same as smoke test but for production
}
```

**What happens:**
- Verifies production endpoints
- Ensures zero-downtime deployment
- Validates service is responding correctly

---

## 🎮 Running the Pipeline

### Method 1: Create Pipeline Job

1. **New Item**
   - Click "New Item" in Jenkins dashboard
   - Enter name: `Flask-CI-CD-Pipeline`
   - Select: **Pipeline**
   - Click **OK**

2. **Configure Pipeline**
   - **General**: Check "GitHub project" (optional)
     - Project URL: `https://github.com/username/repo`
   
   - **Build Triggers**: Check "Poll SCM" or "GitHub hook trigger"
     - Schedule: `H/5 * * * *` (poll every 5 minutes)
   
   - **Pipeline**:
     - Definition: **Pipeline script from SCM**
     - SCM: **Git**
     - Repository URL: `https://github.com/username/repo.git`
     - Credentials: Add GitHub credentials if private
     - Branch Specifier: `*/main` (or `*/*` for all branches)
     - Script Path: `Jenkinsfile`

3. **Save**

### Method 2: Multibranch Pipeline (Recommended)

1. **New Item**
   - Name: `Flask-CI-CD-Multibranch`
   - Type: **Multibranch Pipeline**
   - Click **OK**

2. **Configure**
   - **Branch Sources**: Add source → Git
     - Project Repository: `https://github.com/username/repo.git`
     - Credentials: Add if needed
   
   - **Build Configuration**:
     - Mode: by Jenkinsfile
     - Script Path: `Jenkinsfile`
   
   - **Scan Multibranch Pipeline Triggers**:
     - Check "Periodically if not otherwise run"
     - Interval: 5 minutes

3. **Save**

### Triggering Builds

#### Manual Trigger:
1. Go to pipeline
2. Click **Build Now** (specific branch) or **Scan Multibranch Pipeline Now**

#### Automatic Trigger - Push to Main/Staging:
```bash
# For staging deployment
git checkout staging
git merge main
git push origin staging
# Jenkins automatically builds and deploys to staging

# For production deployment
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
# Jenkins automatically builds and deploys to production
```

#### GitHub Webhook (Real-time):
1. **GitHub Repository** → Settings → Webhooks
2. Add webhook:
   - Payload URL: `http://your-jenkins:8080/github-webhook/`
   - Content type: `application/json`
   - Events: "Just the push event"
   - Active: ✓
3. **Save**

Now pushes trigger Jenkins immediately!

---

## 📧 Email Notifications

### Success Email

```html
Subject: SUCCESS: Job 'Flask-CI-CD-Pipeline [12]'

SUCCESSFUL: Job 'Flask-CI-CD-Pipeline [12]':
Check console output at "Flask-CI-CD-Pipeline [12]"

Build Details:
• Build Number: 12
• Build Status: SUCCESS
• Branch: staging
• Build URL: http://jenkins:8080/job/Flask-CI-CD-Pipeline/12/
```

### Failure Email

```html
Subject: FAILED: Job 'Flask-CI-CD-Pipeline [13]'

FAILED: Job 'Flask-CI-CD-Pipeline [13]':
Check console output at "Flask-CI-CD-Pipeline [13]"

Build Details:
• Build Number: 13
• Build Status: FAILURE
• Branch: main
• Build URL: http://jenkins:8080/job/Flask-CI-CD-Pipeline/13/

Please check the build logs for more details.
```

### Configure Recipients

Edit `Jenkinsfile`:

```groovy
environment {
    EMAIL_RECIPIENTS = 'team@example.com,dev@example.com'  // Multiple recipients
}
```

---

## 🔍 Troubleshooting

### ❌ Pipeline Fails at Setup Environment

**Error**: `python3: command not found`

**Solution**:
```bash
# On Jenkins server
sudo apt install -y python3 python3-venv python3-pip

# Verify
python3 --version
```

### ❌ Tests Fail

**Error**: `ModuleNotFoundError: No module named 'pytest'`

**Solution**:
- Ensure `requirements.txt` includes pytest
- Check virtual environment is activated
- Verify Build stage completed successfully

### ❌ SSH Deployment Fails

**Error**: `Permission denied (publickey)`

**Solution**:
1. Verify SSH key added to Jenkins credentials
2. Verify public key added to server's `~/.ssh/authorized_keys`
3. Test SSH connection manually from Jenkins server
4. Check credential ID matches Jenkinsfile

### ❌ Email Not Sent

**Error**: No email received

**Solution**:
1. **Manage Jenkins** → **Configure System** → **Extended E-mail Notification**
2. Verify SMTP settings
3. Test configuration
4. Check spam folder
5. For Gmail, use App Password not account password

### ❌ Coverage Report Not Published

**Error**: `ERROR: Specified HTML directory does not exist`

**Solution**:
- Ensure pytest runs with `--cov-report=html`
- Verify `htmlcov/` directory created
- Check workspace for coverage files

### ❌ Service Restart Fails on Server

**Error**: `Failed to restart flask-app.service`

**SSH to server and check:**
```bash
# Check service status
sudo systemctl status flask-app

# Check logs
sudo journalctl -u flask-app -n 50

# Verify service file exists
ls -la /etc/systemd/system/flask-app.service

# Test manual restart
sudo systemctl restart flask-app
```

---

## 📊 Comparison with GitHub Actions

| Feature | Jenkins | GitHub Actions |
|---------|---------|----------------|
| **Hosting** | Self-hosted | Cloud-hosted |
| **Cost** | Free (self-hosted) | Free tier: 2000 min/month |
| **Setup Complexity** | Higher (install, configure) | Lower (ready to use) |
| **Customization** | Very high | Moderate |
| **Deployment** | SSH to servers | SSH to servers |
| **Plugins** | 1800+ plugins | GitHub Marketplace |
| **Build Time** | 8-12 minutes | 5-10 minutes |
| **Artifact Storage** | On Jenkins server | GitHub (limited) |
| **Email Notifications** | Built-in | Third-party action |
| **UI/UX** | Classic Jenkins UI | Modern GitHub UI |
| **Integration** | Any Git provider | GitHub only |
| **Best For** | Enterprise, on-prem | GitHub projects, startups |

**Both workflows in this project achieve the same goals with different approaches!**

---

## 📚 Additional Resources

### Documentation
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Plugins](https://plugins.jenkins.io/)
- [AWS EC2 Setup Guide](docs/AWS_EC2_SETUP.md)
- [Email Notification Setup](docs/EMAIL_NOTIFICATION_SETUP.md)

### Related Files
- [Jenkinsfile](Jenkinsfile) - Pipeline definition
- [GitHub Actions Workflow](.github/workflows/ci-cd.yml)
- [Flask Application](app.py)
- [Tests](test_app.py)

### Jenkins Training
- [Jenkins Getting Started](https://www.jenkins.io/doc/pipeline/tour/getting-started/)
- [Pipeline Tutorial](https://www.jenkins.io/doc/book/pipeline/getting-started/)
- [Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)

---

## ✅ Quick Reference

### Common Commands

```bash
# On Jenkins server - check Python
python3 --version
pip3 --version

# View Jenkins logs
sudo journalctl -u jenkins -f

# Restart Jenkins
sudo systemctl restart jenkins

# Check Jenkins status
sudo systemctl status jenkins

# Access Jenkins config
sudo nano /etc/default/jenkins
```

### Pipeline Triggers

```bash
# Trigger staging deployment
git checkout staging
git merge main
git push origin staging

# Trigger production deployment
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# View all tags
git tag -l
```

### Useful Jenkins URLs

- **Dashboard**: `http://jenkins:8080/`
- **Manage Jenkins**: `http://jenkins:8080/manage`
- **Plugin Manager**: `http://jenkins:8080/pluginManager/`
- **Credentials**: `http://jenkins:8080/credentials/`
- **System Log**: `http://jenkins:8080/log/all`

### Build Badge

Add to README.md:

```markdown
[![Build Status](http://jenkins:8080/buildStatus/icon?job=Flask-CI-CD-Pipeline)](http://jenkins:8080/job/Flask-CI-CD-Pipeline/)
```

---

## 🎯 Best Practices

### 1. Security
- ✅ Store credentials in Jenkins Credentials Manager
- ✅ Use separate SSH keys for staging and production
- ✅ Rotate credentials every 90 days
- ✅ Limit Jenkins user permissions
- ✅ Enable HTTPS for Jenkins UI

### 2. Pipeline Optimization
- ✅ Use workspace cleanup to save disk space
- ✅ Cache dependencies when possible
- ✅ Run tests in parallel (if multiple test files)
- ✅ Fail fast on critical errors
- ✅ Use stages for better visualization

### 3. Deployment
- ✅ Always run smoke tests after deployment
- ✅ Keep previous artifacts for rollback
- ✅ Use semantic versioning for production tags
- ✅ Test on staging before production
- ✅ Monitor logs after deployment

### 4. Maintenance
- ✅ Regular Jenkins plugin updates
- ✅ Monitor disk space (artifacts can grow)
- ✅ Review and clean old builds
- ✅ Backup Jenkins home directory
- ✅ Document custom configurations

---

**🚀 Your Jenkins CI/CD pipeline is configured and ready!**

Push to `staging` branch for staging deployment, or create a tag `v*.*.*` for production deployment. Jenkins will handle the rest! 🎉
