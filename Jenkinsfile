pipeline {
    agent any

    environment {
        APP_PORT = '5000'
        GIT_BRANCH = 'guia-3.4.2'
    }

    stages {
        stage('Build') {
            steps {
                echo '=== ETAPA 1: BUILD (Entorno virtual y compilación) ==='
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                    ./venv/bin/python -m py_compile app.py test_app.py
                '''
            }
        }

        stage('Test') {
            steps {
                echo '=== ETAPA 2: TEST (Pruebas unitarias) ==='
                sh '''
                    ./venv/bin/python -m unittest discover -v
                '''
            }
        }

        stage('Generate Documentation') {
            steps {
                echo '=== ETAPA 3: GENERATE DOCUMENTATION (Doxygen) ==='
                sh '''
                    doxygen --version
                    rm -rf docs
                    doxygen Doxyfile
                    test -f docs/html/index.html
                    echo "Documentación HTML generada correctamente en docs/html/"
                '''
            }
        }

        stage('Version Control') {
            steps {
                echo '=== ETAPA 4: VERSION CONTROL (Actualización de trazabilidad en Git) ==='
                withCredentials([usernamePassword(
                    credentialsId: 'github-token-dso',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                        git config user.name "Jenkins CI"
                        git config user.email "jenkins-ci@local.lab"
                        git checkout -B ${GIT_BRANCH}
                        git add docs/
                        if git diff --cached --quiet; then
                            echo "Sin cambios nuevos en la documentación para confirmar."
                        else
                            git commit -m "Docs: Actualiza documentación Doxygen [Build #${BUILD_NUMBER}]"
                            git push https://${GIT_USER}:${GIT_TOKEN}@github.com/BastianEd/test-C-D.git ${GIT_BRANCH}
                        fi
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '=== ETAPA 5: DEPLOY (Despliegue controlado en entorno de prueba) ==='
                sh '''
                    pkill -f "python app.py" || true
                    nohup ./venv/bin/python app.py > flask-342.log 2>&1 &
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
            sh '''
                pkill -f "python app.py" || true
                tar -czf docs-doxygen-build-${BUILD_NUMBER}.tar.gz docs/ || true
            '''
            archiveArtifacts artifacts: 'docs-doxygen-build-*.tar.gz, flask-342.log', allowEmptyArchive: true
        }
        success {
            echo 'PIPELINE DE DOCUMENTACIÓN Y TRAZABILIDAD COMPLETADO EXITOSAMENTE'
        }
        failure {
            echo 'ALERTA DE TRAZABILIDAD: El pipeline falló. Revisar generación Doxygen o sincronización Git.'
        }
    }
}
