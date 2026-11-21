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
                sh """
                    docker rm -f smoke_app_${BUILD_NUMBER} || true
                    docker run -d --name smoke_app_${BUILD_NUMBER} ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 20
                    docker exec smoke_app_${BUILD_NUMBER} python -c "import urllib.request; resp = urllib.request.urlopen('http://localhost:5000/').read().decode(); print(resp); assert 'OK' in resp"
                """
            }
            post {
                always {
                    sh "docker rm -f smoke_app_${BUILD_NUMBER} || true"
                }
            }
        }
    }
}