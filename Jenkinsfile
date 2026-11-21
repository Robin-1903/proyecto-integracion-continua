pipeline {
    agent any

    environment {
        IMAGE_NAME = "proyecto-integracion-continua"
    }

    stages {
        stage('Pruebas unitarias') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root:root'
                    reuseNode true
                }
            }
            steps {
                sh '''
                    pip install --no-cache-dir -r app/requirements.txt
                    pytest -v app/tests --junitxml=reporte-pruebas.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reporte-pruebas.xml'
                }
            }
        }

        stage('Construir imagen') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ./app"
            }
        }

        stage('Prueba de humo') {
            steps {
                sh '''
                    docker rm -f smoke_app_${BUILD_NUMBER} || true
                    docker run -d --name smoke_app_${BUILD_NUMBER} ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 15
                    docker logs smoke_app_${BUILD_NUMBER}
                    docker exec smoke_app_${BUILD_NUMBER} python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/').read().decode())"
                '''
            }
            post {
                always {
                    sh "docker rm -f smoke_app_\${BUILD_NUMBER} || true"
                }
            }
        }
    }
}