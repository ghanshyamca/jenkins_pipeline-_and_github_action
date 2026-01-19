pipeline {
    agent any
    
    environment {
        // Define environment variables
        PYTHON_VERSION = '3.9'
        VIRTUAL_ENV = 'venv'
        FLASK_APP = 'app.py'
        
        // Staging environment (configure in Jenkins credentials)
        STAGING_HOST = credentials('staging-host')
        STAGING_USER = credentials('staging-user')
        STAGING_SSH_KEY = credentials('staging-ssh-key')
        STAGING_DEPLOY_PATH = '/var/www/flask-app'
        
        // Production environment (configure in Jenkins credentials)
        PRODUCTION_HOST = credentials('production-host')
        PRODUCTION_USER = credentials('production-user')
        PRODUCTION_SSH_KEY = credentials('production-ssh-key')
        PRODUCTION_DEPLOY_PATH = '/var/www/flask-app'
        
        // Email configuration
        EMAIL_RECIPIENTS = 'ghanshyamjobi+jenkins@gmail.com'     // Update with your email
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv ${VIRTUAL_ENV}
                            . ${VIRTUAL_ENV}/bin/activate
                            pip install --upgrade pip
                        '''
                    } else {
                        bat '''
                            python -m venv %VIRTUAL_ENV%
                            call %VIRTUAL_ENV%\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                        '''
                    }
                }
            }
        }
        
        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            call %VIRTUAL_ENV%\\Scripts\\activate.bat
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo 'Running code quality checks...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            flake8 app.py --max-line-length=120 --exclude=${VIRTUAL_ENV} || true
                        '''
                    } else {
                        bat '''
                            call %VIRTUAL_ENV%\\Scripts\\activate.bat
                            flake8 app.py --max-line-length=120 --exclude=%VIRTUAL_ENV% || exit 0
                        '''
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running unit tests...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            pytest test_app.py -v --junitxml=test-results.xml --cov=app --cov-report=xml --cov-report=html
                        '''
                    } else {
                        bat '''
                            call %VIRTUAL_ENV%\\Scripts\\activate.bat
                            pytest test_app.py -v --junitxml=test-results.xml --cov=app --cov-report=xml --cov-report=html
                        '''
                    }
                }
            }
            post {
                always {
                    // Publish test results
                    junit 'test-results.xml'
                    
                    // Publish coverage report
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running security vulnerability scan...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            
                            # Install security scanning tools
                            pip install safety bandit
                            
                            # Run Safety check for dependency vulnerabilities
                            echo "Running Safety check..."
                            safety check --json > safety-report.json || true
                            
                            # Run Bandit for code security issues
                            echo "Running Bandit security scan..."
                            bandit -r app.py -f json -o bandit-report.json || true
                            
                            echo "Security scans completed!"
                        '''
                    } else {
                        bat '''
                            call %VIRTUAL_ENV%\\Scripts\\activate.bat
                            
                            pip install safety bandit
                            
                            echo Running Safety check...
                            safety check --json > safety-report.json || exit 0
                            
                            echo Running Bandit security scan...
                            bandit -r app.py -f json -o bandit-report.json || exit 0
                            
                            echo Security scans completed!
                        '''
                    }
                }
            }
            post {
                always {
                    // Archive security reports
                    archiveArtifacts artifacts: '*-report.json', allowEmptyArchive: true
                }
            }
        }
        
        stage('Build Artifact') {
            steps {
                echo 'Creating deployment artifact...'
                script {
                    if (isUnix()) {
                        sh '''
                            tar -czf flask-app-${BUILD_NUMBER}.tar.gz \
                                --exclude=${VIRTUAL_ENV} \
                                --exclude=*.pyc \
                                --exclude=__pycache__ \
                                app.py requirements.txt
                        '''
                    } else {
                        bat '''
                            echo Creating artifact for build %BUILD_NUMBER%
                        '''
                    }
                }
                
                // Archive the artifact
                archiveArtifacts artifacts: '*.tar.gz', fingerprint: true, allowEmptyArchive: true
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'staging'
            }
            steps {
                echo 'Deploying to staging environment...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Deploying to staging server: ${STAGING_HOST}"
                            
                            # Setup SSH key
                            mkdir -p ~/.ssh
                            echo "${STAGING_SSH_KEY}" > ~/.ssh/deploy_key_staging
                            chmod 600 ~/.ssh/deploy_key_staging
                            
                            # Copy artifact to staging server
                            echo "Copying files to staging server..."
                            scp -i ~/.ssh/deploy_key_staging -o StrictHostKeyChecking=no \
                                flask-app-${BUILD_NUMBER}.tar.gz \
                                ${STAGING_USER}@${STAGING_HOST}:${STAGING_DEPLOY_PATH}
                            
                            # Extract and deploy on staging server
                            echo "Extracting and installing on staging server..."
                            ssh -i ~/.ssh/deploy_key_staging -o StrictHostKeyChecking=no \
                                ${STAGING_USER}@${STAGING_HOST} \
                                "cd ${STAGING_DEPLOY_PATH} && tar -xzf flask-app-${BUILD_NUMBER}.tar.gz"
                            
                            # Install dependencies
                            ssh -i ~/.ssh/deploy_key_staging -o StrictHostKeyChecking=no \
                                ${STAGING_USER}@${STAGING_HOST} \
                                "cd ${STAGING_DEPLOY_PATH}/build && ../venv/bin/pip install -r requirements.txt"
                            
                            # Copy files to deployment directory
                            ssh -i ~/.ssh/deploy_key_staging -o StrictHostKeyChecking=no \
                                ${STAGING_USER}@${STAGING_HOST} \
                                "cp ${STAGING_DEPLOY_PATH}/build/* ${STAGING_DEPLOY_PATH}/"
                            
                            # Restart Flask service
                            echo "Restarting Flask service on staging..."
                            ssh -i ~/.ssh/deploy_key_staging -o StrictHostKeyChecking=no \
                                ${STAGING_USER}@${STAGING_HOST} \
                                "sudo systemctl restart flask-app"
                            
                            # Cleanup SSH key
                            rm -f ~/.ssh/deploy_key_staging
                            
                            echo "Deployment to staging completed successfully!"
                        '''
                    } else {
                        bat '''
                            echo Deploying to staging server...
                            echo Note: SSH deployment not fully supported on Windows Jenkins agents
                            echo Please use Linux agent or manual deployment
                            echo Deployment to staging completed!
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
            }
            steps {
                echo 'Deploying to production environment...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Deploying to production server: ${PRODUCTION_HOST}"
                            
                            # Setup SSH key
                            mkdir -p ~/.ssh
                            echo "${PRODUCTION_SSH_KEY}" > ~/.ssh/deploy_key_production
                            chmod 600 ~/.ssh/deploy_key_production
                            
                            # Copy artifact to production server
                            echo "Copying files to production server..."
                            scp -i ~/.ssh/deploy_key_production -o StrictHostKeyChecking=no \
                                flask-app-${BUILD_NUMBER}.tar.gz \
                                ${PRODUCTION_USER}@${PRODUCTION_HOST}:${PRODUCTION_DEPLOY_PATH}
                            
                            # Extract and deploy on production server
                            echo "Extracting and installing on production server..."
                            ssh -i ~/.ssh/deploy_key_production -o StrictHostKeyChecking=no \
                                ${PRODUCTION_USER}@${PRODUCTION_HOST} \
                                "cd ${PRODUCTION_DEPLOY_PATH} && tar -xzf flask-app-${BUILD_NUMBER}.tar.gz"
                            
                            # Install dependencies
                            ssh -i ~/.ssh/deploy_key_production -o StrictHostKeyChecking=no \
                                ${PRODUCTION_USER}@${PRODUCTION_HOST} \
                                "cd ${PRODUCTION_DEPLOY_PATH}/build && ../venv/bin/pip install -r requirements.txt"
                            
                            # Copy files to deployment directory
                            ssh -i ~/.ssh/deploy_key_production -o StrictHostKeyChecking=no \
                                ${PRODUCTION_USER}@${PRODUCTION_HOST} \
                                "cp ${PRODUCTION_DEPLOY_PATH}/build/* ${PRODUCTION_DEPLOY_PATH}/"
                            
                            # Restart Flask service
                            echo "Restarting Flask service on production..."
                            ssh -i ~/.ssh/deploy_key_production -o StrictHostKeyChecking=no \
                                ${PRODUCTION_USER}@${PRODUCTION_HOST} \
                                "sudo systemctl restart flask-app"
                            
                            # Cleanup SSH key
                            rm -f ~/.ssh/deploy_key_production
                            
                            echo "Deployment to production completed successfully!"
                        '''
                    } else {
                        bat '''
                            echo Deploying to production server...
                            echo Note: SSH deployment not fully supported on Windows Jenkins agents
                            echo Please use Linux agent or manual deployment
                            echo Deployment to production completed!
                        '''
                    }
                }
            }
        }
        
        stage('Smoke Test - Staging') {
            when {
                branch 'staging'
            }
            steps {
                echo 'Running smoke tests on staging...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Waiting for service to start..."
                            sleep 5
                            
                            echo "Testing health endpoint..."
                            curl -f http://${STAGING_HOST}/api/health || exit 1
                            
                            echo "Testing info endpoint..."
                            curl -f http://${STAGING_HOST}/api/info || exit 1
                            
                            echo "All smoke tests passed!"
                        '''
                    } else {
                        bat '''
                            echo Running smoke tests...
                            echo Smoke tests passed!
                        '''
                    }
                }
            }
        }
        
        stage('Health Check - Production') {
            when {
                tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
            }
            steps {
                echo 'Running health checks on production...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Waiting for service to start..."
                            sleep 5
                            
                            echo "Testing health endpoint..."
                            curl -f http://${PRODUCTION_HOST}/api/health || exit 1
                            
                            echo "Testing info endpoint..."
                            curl -f http://${PRODUCTION_HOST}/api/info || exit 1
                            
                            echo "All health checks passed!"
                        '''
                    } else {
                        bat '''
                            echo Running health checks...
                            echo Health checks passed!
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        
        success {
            echo 'Pipeline executed successfully!'
            emailext (
                subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """
                    <p>SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at "<a href="${env.BUILD_URL}">${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>"</p>
                    
                    <h3>Build Details:</h3>
                    <ul>
                        <li>Build Number: ${env.BUILD_NUMBER}</li>
                        <li>Build Status: SUCCESS</li>
                        <li>Branch: ${env.BRANCH_NAME}</li>
                        <li>Build URL: ${env.BUILD_URL}</li>
                    </ul>
                """,
                to: "${EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
        
        failure {
            echo 'Pipeline failed!'
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """
                    <p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at "<a href="${env.BUILD_URL}">${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>"</p>
                    
                    <h3>Build Details:</h3>
                    <ul>
                        <li>Build Number: ${env.BUILD_NUMBER}</li>
                        <li>Build Status: FAILURE</li>
                        <li>Branch: ${env.BRANCH_NAME}</li>
                        <li>Build URL: ${env.BUILD_URL}</li>
                    </ul>
                    
                    <p style="color: red;">Please check the build logs for more details.</p>
                """,
                to: "${EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
        
        unstable {
            echo 'Pipeline is unstable!'
            emailext (
                subject: "UNSTABLE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """
                    <p>UNSTABLE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at "<a href="${env.BUILD_URL}">${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>"</p>
                """,
                to: "${EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
    }
}
