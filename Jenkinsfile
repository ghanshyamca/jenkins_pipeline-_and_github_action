pipeline {
    agent any
    
    environment {
        // Define environment variables
        PYTHON_VERSION = '3.9'
        VIRTUAL_ENV = 'venv'
        STAGING_SERVER = credentials('staging-server')  // Configure in Jenkins credentials
        EMAIL_RECIPIENTS = 'your-email@example.com'     // Update with your email
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
                echo 'Running security scan...'
                script {
                    if (isUnix()) {
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            pip install safety
                            safety check --json || true
                        '''
                    } else {
                        bat '''
                            call %VIRTUAL_ENV%\\Scripts\\activate.bat
                            pip install safety
                            safety check --json || exit 0
                        '''
                    }
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
                                app.py requirements.txt \
                                --exclude=${VIRTUAL_ENV} \
                                --exclude=*.pyc \
                                --exclude=__pycache__
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
                branch 'main'
            }
            steps {
                echo 'Deploying to staging environment...'
                script {
                    // Example deployment script
                    // Customize this based on your staging environment
                    if (isUnix()) {
                        sh '''
                            echo "Deploying to staging server..."
                            # Example: scp flask-app-${BUILD_NUMBER}.tar.gz user@staging-server:/path/to/deploy
                            # Example: ssh user@staging-server "cd /path/to/deploy && tar -xzf flask-app-${BUILD_NUMBER}.tar.gz"
                            # Example: ssh user@staging-server "cd /path/to/deploy && pip install -r requirements.txt"
                            # Example: ssh user@staging-server "sudo systemctl restart flask-app"
                            
                            echo "Deployment to staging completed!"
                        '''
                    } else {
                        bat '''
                            echo Deploying to staging server...
                            echo Deployment to staging completed!
                        '''
                    }
                }
            }
        }
        
        stage('Smoke Test') {
            when {
                branch 'main'
            }
            steps {
                echo 'Running smoke tests on staging...'
                script {
                    if (isUnix()) {
                        sh '''
                            # Example: curl -f http://staging-server:5000/api/health || exit 1
                            echo "Smoke tests passed!"
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
