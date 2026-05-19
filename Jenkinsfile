pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/1by23is090-netizen/quizverse_enhanced.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Initialize Database') {
            steps {
                bat 'python init_db.py'
            }
        }

        stage('Run Application') {
            steps {
                bat 'python app.py'
            }
        }
    }
}