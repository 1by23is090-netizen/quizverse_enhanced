pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/1by23is090-netizen/quizverse_enhanced.git'
            }
        }

        stage('Done') {
            steps {
                bat 'echo Build Successful'
            }
        }
    }
}