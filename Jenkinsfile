pipeline {
    agent any

    triggers { githubPush() }

    environment {
        IMAGE_NAME           = 'aldik15/jenkins-flask-mysql'
        IMAGE_TAG            = "${BUILD_NUMBER}"
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
        COMPOSE_PROJECT_NAME = 'flaskdb'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build') {
            steps {
                bat 'echo Mulai build aplikasi nomor %BUILD_NUMBER%'
                bat 'docker --version'
                bat 'docker compose config -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% -t %IMAGE_NAME%:latest .'
                bat 'docker build -t %IMAGE_NAME%-db:%IMAGE_TAG% ./db'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: REGISTRY_CREDENTIALS,
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    bat 'echo %PASS%| docker login -u %USER% --password-stdin'
                    bat 'docker push %IMAGE_NAME%:%IMAGE_TAG%'
                    bat 'docker push %IMAGE_NAME%:latest'
                    bat 'docker push %IMAGE_NAME%-db:%IMAGE_TAG%'
                }
            }
        }

        stage('Deploy (App + Database)') {
            steps {
                bat 'docker compose up -d --wait'
                bat 'docker compose ps'
            }
        }
    }

    post {
        always  { bat 'docker logout' }
        success { echo 'Pipeline sukses: aplikasi dan database berjalan di port 5000' }
        failure { echo 'Pipeline gagal, cek Console Output' }
    }
}
