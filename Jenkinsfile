pipeline {
  agent any
  environment {
    DOCKERHUB_CREDENTIALS = 'docker-hub-creds' // Jenkins credential ID for Docker Hub
    DOCKERHUB_REPO = 'madhavsanjaypatil/scientific-calc' // Docker Hub repo
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install deps & Test') {
      steps {
          sh '''
            python3 -m venv venv
            venv/bin/pip install --upgrade pip
            venv/bin/pip install -r requirements.txt
            venv/bin/pytest -q
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
        withCredentials([usernamePassword(
            credentialsId: env.DOCKERHUB_CREDENTIALS, 
            usernameVariable: 'DOCKER_USER', 
            passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          sh "docker push ${env.IMAGE_TAG}"
        }
      }
    }

    stage('Deploy via Ansible') {
      steps {
        sh "ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --extra-vars \"image=${env.IMAGE_TAG}\""
      }
    }
  }

  post {
    success { echo 'Pipeline succeeded' }
    failure { echo 'Pipeline failed' }
  }
}
