pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'docker-hub-creds'
    DOCKERHUB_REPO = 'madhavsanjaypatil/scientific-calc'
    RECIPIENT_EMAIL = 'dev-team@yourcompany.com'  // Add your email here
  }

  stages {

    stage('Checkout') {
      steps {
        echo 'Checking out source code...'
        checkout scm
      }
    }

    stage('Install deps & Test') {
      steps {
        echo 'Installing dependencies and running tests...'
        sh '''
          python3 -m pip install --break-system-packages --user -r requirements.txt
          python3 -m pytest -q
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          def tag = "${env.BUILD_ID}"
          sh "docker build -t ${DOCKERHUB_REPO}:${tag} ."
          env.IMAGE_TAG = "${DOCKERHUB_REPO}:${tag}"
        }
      }
    }

    stage('Docker Login & Push') {
      steps {
        echo 'Logging into Docker Hub and pushing image...'
        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          sh "docker push ${env.IMAGE_TAG}"
        }
      }
    }

    stage('Deploy via Ansible') {
      steps {
        echo 'Deploying container using Ansible...'
        sh "ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --extra-vars \"image=${env.IMAGE_TAG}\""
      }
    }

  } // end stages

  post {
    always {
      echo "Build completed with status: ${currentBuild.currentResult}"
      echo "Build URL: ${env.BUILD_URL}"
      echo "Duration: ${currentBuild.durationString}"
    }
    
    success {
      script {
        emailext (
          subject: "SUCCESS - Build #${env.BUILD_NUMBER} - ${env.JOB_NAME}",
          body: """
          ✅ BUILD SUCCESSFUL ✅
          
          Project: ${env.JOB_NAME}
          Build Number: ${env.BUILD_NUMBER}
          Build URL: ${env.BUILD_URL}
          Docker Image: ${env.IMAGE_TAG ?: 'N/A'}
          Duration: ${currentBuild.durationString}
          
          All stages completed successfully!
          
          The application has been deployed with the new Docker image: ${env.IMAGE_TAG}
          
          ---
          This is an automated message from Jenkins CI/CD
          """,
          to: "${env.RECIPIENT_EMAIL}",
          attachLog: false
        )
      }
    }
    
    failure {
      script {
        emailext (
          subject: "FAILED - Build #${env.BUILD_NUMBER} - ${env.JOB_NAME}",
          body: """
          ❌ BUILD FAILED ❌
          
          Project: ${env.JOB_NAME}
          Build Number: ${env.BUILD_NUMBER}
          Build URL: ${env.BUILD_URL}
          Duration: ${currentBuild.durationString}
          Docker Image: ${env.IMAGE_TAG ?: 'N/A'}
          
          Please check the build logs for details: ${env.BUILD_URL}console
          
          ---
          This is an automated message from Jenkins CI/CD
          """,
          to: "${env.RECIPIENT_EMAIL}",
          attachLog: true,  // Attach build log for failures
          compressLog: true
        )
      }
    }
    
    unstable {
      script {
        emailext (
          subject: "UNSTABLE - Build #${env.BUILD_NUMBER} - ${env.JOB_NAME}",
          body: """
          ⚠️ BUILD UNSTABLE ⚠️
          
          Project: ${env.JOB_NAME}
          Build Number: ${env.BUILD_NUMBER}
          Build URL: ${env.BUILD_URL}
          Duration: ${currentBuild.durationString}
          Docker Image: ${env.IMAGE_TAG ?: 'N/A'}
          
          Build completed but with test failures or other issues.
          
          Please check the build logs: ${env.BUILD_URL}console
          
          ---
          This is an automated message from Jenkins CI/CD
          """,
          to: "${env.RECIPIENT_EMAIL}",
          attachLog: false
        )
      }
    }
    
    aborted {
      script {
        emailext (
          subject: "ABORTED - Build #${env.BUILD_NUMBER} - ${env.JOB_NAME}",
          body: """
          🛑 BUILD ABORTED 🛑
          
          Project: ${env.JOB_NAME}
          Build Number: ${env.BUILD_NUMBER}
          Build URL: ${env.BUILD_URL}
          Duration: ${currentBuild.durationString}
          
          Build was manually aborted.
          
          ---
          This is an automated message from Jenkins CI/CD
          """,
          to: "${env.RECIPIENT_EMAIL}",
          attachLog: false
        )
      }
    }
  }
}
