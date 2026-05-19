pipeline {
    agent any

    environment {
        IMAGE_NAME  = 'quizverse-app'
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        CONTAINER   = 'quizverse-running'
        PORT        = '5000'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'YOUR_GITHUB_REPO_URL'
            }
        }

        stage('Lint / Syntax Check') {
            steps {
                sh 'python -m py_compile app.py init_db.py'
                echo 'Syntax check passed.'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'docker tag  ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                    docker stop ${CONTAINER} || true
                    docker rm   ${CONTAINER} || true
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker run -d \
                        --name  ${CONTAINER} \
                        -p      ${PORT}:5000 \
                        -e      SECRET_KEY=${SECRET_KEY} \
                        --restart unless-stopped \
                        ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Health Check') {
            steps {
                sleep 4
                sh "curl -f http://localhost:${PORT}/ || (docker logs ${CONTAINER} && exit 1)"
            }
        }

    }

    post {
        success {
            echo "✅ QuizVerse deployed successfully on port ${PORT}."
        }
        failure {
            echo "❌ Deployment failed. Check the logs above."
            sh "docker logs ${CONTAINER} || true"
        }
        always {
            // Remove dangling images to save space
            sh 'docker image prune -f || true'
        }
    }
}
