pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'docker-hub-creds'   // Jenkins credentials ID for DockerHub
    DOCKERHUB_REPO = 'madhavsanjaypatil/scientific-calc'  // Change if needed
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
  }

  post {
    success {
      echo 'Pipeline succeeded!'
      emailext(
        to: 'madhavspatil07@gmail.com, drpatils@hotmail.com',  // Add multiple recipients here
        subject: "✅ SUCCESS: Scientific Calculator Pipeline #${env.BUILD_NUMBER}",
        body: """
          <h3>🎉 Jenkins Pipeline Successful!</h3>
          <p><b>Repository:</b> ${env.GIT_URL}</p>
          <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>
          <p><b>Docker Image:</b> ${env.IMAGE_TAG}</p>
          <p>The image has been successfully pushed to Docker Hub and deployed via Ansible.</p>
          <p>Visit Docker Hub: <a href="https://hub.docker.com/repository/docker/madhavsanjaypatil/scientific-calc">View Image</a></p>
        """,
        mimeType: 'text/html'
      )
    }

    failure {
      echo 'Pipeline failed!'
      emailext(
        to: 'madhavspatil07@gmail.com, drpatils@hotmail.com',
        subject: "❌ FAILURE: Scientific Calculator Pipeline #${env.BUILD_NUMBER}",
        body: """
          <h3>🚨 Jenkins Pipeline Failed</h3>
          <p><b>Repository:</b> ${env.GIT_URL}</p>
          <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>
          <p>Please check the Jenkins logs for detailed failure reasons.</p>
        """,
        mimeType: 'text/html'
      )
    }
  }
}
