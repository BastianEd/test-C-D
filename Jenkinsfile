pipeline {
    agent any

    environment {
        APP_PORT = '5000'
        ZAP_API  = 'http://172.17.0.1:8090'
    }

    stages {
        stage('Build') {
            steps {
                echo '=== ETAPA 1: BUILD (Entorno virtual y compilación) ==='
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                    ./venv/bin/python -m py_compile app.py test_hola.py
                '''
            }
        }

        stage('Test') {
            steps {
                echo '=== ETAPA 2: TEST (Pruebas unitarias) ==='
                sh './venv/bin/python -m unittest discover -v'
            }
        }

        stage('Analyze') {
            steps {
                echo '=== ETAPA 3: ANALYZE (Análisis estático SAST con SonarQube) ==='
                script {
                    def scannerHome = tool 'SonarScanner-DSO'
                    withSonarQubeEnv('SonarQube-DSO') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '=== ETAPA 4: DEPLOY (Despliegue de prueba para OWASP ZAP) ==='
                sh '''
                    pkill -f "python app.py" || true
                    nohup ./venv/bin/python app.py > flask.log 2>&1 &
                    sleep 3
                    curl -s "http://localhost:${APP_PORT}/hello?name=TEST"
                '''
            }
        }

        stage('Security Test') {
            steps {
                echo '=== ETAPA 5: SECURITY TEST (SCA Dependency-Check + DAST OWASP ZAP) ==='
                dependencyCheck additionalArguments: '--scan ./ --exclude "**/venv/**" --format HTML --format XML --out ./', odcInstallation: 'Dependency-Check-DSO'

                sh '''
                    APP_IP=$(hostname -i | awk '{print $1}')
                    TARGET_URL="http://${APP_IP}:${APP_PORT}/hello?name=TEST"
                    echo "Escaneando objetivo dinámico: ${TARGET_URL}"

                    # 1. Spider (rastreo de rutas)
                    curl -s "${ZAP_API}/JSON/spider/action/scan/?url=${TARGET_URL}"
                    sleep 5

                    # 2. Active Scan (búsqueda activa de vulnerabilidades como XSS)
                    curl -s "${ZAP_API}/JSON/ascan/action/scan/?url=${TARGET_URL}"
                    sleep 15

                    # 3. Descargar reporte HTML generado por ZAP
                    curl -s "${ZAP_API}/OTHER/core/other/htmlreport/" -o zap-report.html
                    ls -lh dependency-check-report.html zap-report.html
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dependency-check-report.html, zap-report.html', allowEmptyArchive: true
            sh 'pkill -f "python app.py" || true'
        }
        success {
            echo 'PIPELINE DEVSECOPS COMPLETADO EXITOSAMENTE'
        }
        failure {
            echo 'EL PIPELINE FINALIZÓ CON ERRORES - REVISAR CONSOLA'
        }
    }
}
