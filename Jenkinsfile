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
            emailext subject: "✅ Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     body: """<p>The Anime Recommender project was deployed successfully.</p>
                              <p><b>Job:</b> ${env.JOB_NAME}<br>
                                 <b>Build:</b> #${env.BUILD_NUMBER}<br>
                                 <b>URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>""",
                     mimeType: 'text/html',
                     to: "gaganbublu2005@gmail.com"
        }
        failure {
            echo '❌ Something went wrong.'
            emailext subject: "❌ Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     body: """<p>The build failed.</p>
                              <p><b>Job:</b> ${env.JOB_NAME}<br>
                                 <b>Build:</b> #${env.BUILD_NUMBER}<br>
                                 <b>URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>""",
                     mimeType: 'text/html',
                     to: "gaganbublu2005@gmail.com"
        }
    }
}
