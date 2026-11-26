pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        echo 'ETAPA 1: BUILD'
        sh 'python3 -m py_compile *.py'
      }
    }

    stage('Test') {
      steps {
        echo 'ETAPA 2: TEST'
        sh 'python3 -m unittest discover -v'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        echo 'ETAPA 3: ANALISIS ESTATICO (SAST) CON SONARQUBE'
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
        echo 'ETAPA 4: DEPLOY'
        sh '''
          mkdir -p despliegue
          cp *.py despliegue/
          ls -la despliegue/
        '''
      }
    }
  }

  post {
    success {
      echo 'PIPELINE COMPLETADO CORRECTAMENTE'
    }
    failure {
      echo 'ERROR EN LA EJECUCION DEL PIPELINE'
    }
  }
}
