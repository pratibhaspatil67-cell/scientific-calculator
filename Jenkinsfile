pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'docker-hub-creds'
    DOCKERHUB_REPO = 'madhavsanjaypatil/scientific-calc'
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
  success {
    emailext (
      subject: "✅ SUCCESS: Scientific Calculator Build #${env.BUILD_NUMBER}",
      body: """
      <p>Build Details:</p>
      <ul>
        <li><b>Build Number:</b> ${env.BUILD_NUMBER}</li>
        <li><b>Job:</b> ${env.JOB_NAME}</li>
        <li><b>Docker Image:</b> ${env.IMAGE_TAG}</li>
        <li><b>Build URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></li>
      </ul>
      """,
      to: 'madhavspatil07@gmail.com',
      mimeType: 'text/html'
    )
  }
  failure {
    emailext (
      subject: "❌ FAILURE: Scientific Calculator Build #${env.BUILD_NUMBER}",
      body: """
      <p>The build has failed. Please check:</p>
      <p><a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
      """,
      to: 'madhavspatil07@gmail.com',
      mimeType: 'text/html'
    )
  }
}


} // end pipeline
