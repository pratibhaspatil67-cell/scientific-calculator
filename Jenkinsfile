pipeline {
  agent {
    docker {
      image 'python:3.9-slim'
      args '-v /home/jenkins:/home/jenkins'
    }
  }
  environment {
    DOCKERHUB_CREDENTIALS = 'docker-hub-creds'
    DOCKERHUB_REPO = 'madhavsanjaypatil/scientific-calc'
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
          python -m venv venv
          . venv/bin/activate
          pip install -r requirements.txt
          pytest -q
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
        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
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
    success { 
      echo 'Pipeline succeeded' 
    }
    failure { 
      echo 'Pipeline failed' 
    }
    always {
      sh 'docker logout'
    }
  }
}
