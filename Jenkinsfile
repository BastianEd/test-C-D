pipeline {
    agent any

    environment {
        PIPENV_VENV_IN_PROJECT = '1'
        APP_PORT = '5000'
    }

    stages {
        stage('Build') {
            steps {
                echo '=== ETAPA 1: BUILD (Compilación y verificación de sintaxis) ==='
                sh '''
                    python3 --version
                    pipenv --version
                    python3 -m py_compile app.py test_app.py
                '''
            }
        }

        stage('Test') {
            steps {
                echo '=== ETAPA 2: TEST (Pruebas unitarias en entorno pipenv) ==='
                sh '''
                    pipenv install --dev
                    pipenv run python -m unittest discover -v
                '''
            }
        }

        stage('Analyze') {
            steps {
                echo '=== ETAPA 3: ANALYZE (Calidad y seguridad SAST con SonarQube) ==='
                script {
                    def scannerHome = tool 'SonarScanner-DSO'
                    withSonarQubeEnv('SonarQube-DSO') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Dependency Management') {
            steps {
                echo '=== ETAPA 4: DEPENDENCY MANAGEMENT (Auditoría y actualización segura) ==='
                sh '''
                    pipenv update
                    pipenv graph
                    pipenv requirements > requirements-locked.txt
                '''
                dependencyCheck additionalArguments: '--scan ./requirements-locked.txt --enableExperimental --noupdate --failOnCVSS 7 --format HTML --out ./', odcInstallation: 'Dependency-Check-DSO'
            }
        }

        stage('Deploy') {
            steps {
                echo '=== ETAPA 5: DEPLOY (Despliegue controlado en entorno de prueba) ==='
                sh '''
                    pkill -f "python app.py" || true
                    nohup pipenv run python app.py > flask-332.log 2>&1 &
                    sleep 3
                    curl -s -f "http://127.0.0.1:${APP_PORT}/"
                    echo ""
                    curl -s -f "http://127.0.0.1:${APP_PORT}/hello?name=DevSecOps"
                    echo ""
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dependency-check-report.html, requirements-locked.txt', allowEmptyArchive: true
            sh 'pkill -f "python app.py" || true'
        }
        success {
            echo 'PIPELINE DE GESTIÓN DE DEPENDENCIAS COMPLETADO EXITOSAMENTE'
        }
        failure {
            echo 'ALERTA: EL PIPELINE FALLÓ - REVISAR CONSOLA Y REPORTES DE SEGURIDAD'
        }
    }
}
