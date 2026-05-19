pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/1by23is090-netizen/quizverse_enhanced.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('enhanced_quiz_system') {
                    bat 'npm install'
                }
            }
        }

        stage('Run Application') {
            steps {
                dir('enhanced_quiz_system') {
                    bat 'npm start'
                }
            }
        }
    }
}