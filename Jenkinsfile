pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "nginx-my-project"
        DOCKER_REGISTRY = "docker.io"  // Например, Docker Hub или ваш частный реестр
        K8S_NAMESPACE = "prod"          // Ваш Kubernetes namespace
        K8S_DEPLOYMENT = "deployment.yml" // Название деплоймента в Kubernetes
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Luferius1/goapp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Собираем Docker образ
                    sh """
                        docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${BUILD_ID} .
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Обновляем деплоймент в Kubernetes
                    sh """
                        kubectl apply -f ${DEPLOYMENT_YAML} -n ${K8S_NAMESPACE}
                    """
                }
            }
        }
    }

    post {
        always {
            // Очистка рабочего пространства
            cleanWs()
        }
    }
}
