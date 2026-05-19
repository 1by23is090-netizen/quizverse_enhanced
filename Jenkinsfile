pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/1by23is090-netizen/quizverse_enhanced.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t quizverse .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker run -d -p 9095:3000 quizverse'
            }
        }
    }
}