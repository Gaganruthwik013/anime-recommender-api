pipeline {
    agent any

    environment {
        IMAGE_NAME = 'anime-recommender'
        CONTAINER_NAME = 'anime-container'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    bat 'docker build -t %IMAGE_NAME% .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    bat 'docker rm -f %CONTAINER_NAME% || exit 0'
                    bat 'docker run -d -p 8501:8501 --name %CONTAINER_NAME% %IMAGE_NAME%'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Anime Recommender Deployed Successfully!'
            emailext (
                subject: '✅ Jenkins Build Successful: Anime Recommender',
                body: "Good news!\n\nYour pipeline executed successfully and the Anime Recommender is deployed.\n\nProject: ${env.JOB_NAME}\nBuild Number: ${env.BUILD_NUMBER}\nCheck: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                to: 'your_email@gmail.com'
            )
        }

        failure {
            echo '❌ Something went wrong.'
            emailext (
                subject: '❌ Jenkins Build FAILED: Anime Recommender',
                body: "Oops, the build failed.\n\nProject: ${env.JOB_NAME}\nBuild Number: ${env.BUILD_NUMBER}\nCheck logs at: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                to: 'your_email@gmail.com'
            )
        }
    }
}
