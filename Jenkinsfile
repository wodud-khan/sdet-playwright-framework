pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install'
            }
        }

        stage('Run Smoke Tests') {
            steps {
                sh 'pytest -m smoke -n auto'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**/*', allowEmptyArchive: true
        }
    }
}
