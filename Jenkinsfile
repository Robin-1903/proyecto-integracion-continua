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
                    docker run -d -e PYTHONUNBUFFERED=1 --name smoke_app_${BUILD_NUMBER} ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker exec smoke_app_${BUILD_NUMBER} python -c "import urllib.request, time, sys
for i in range(20):
    try:
        res = urllib.request.urlopen('http://127.0.0.1:5000/').read().decode()
        print('RESPUESTA_OK:', res)
        sys.exit(0)
    except Exception:
        time.sleep(2)
sys.exit(1)"
                    docker logs smoke_app_${BUILD_NUMBER}
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