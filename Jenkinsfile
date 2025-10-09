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
      echo 'Pipeline succeeded'
      emailext (
        to: 'your_email@gmail.com',
        subject: "✅ SUCCESS: Jenkins Build #${env.BUILD_NUMBER}",
        body: """
        <p>Hi Madhav,</p>
        <p>Your Scientific Calculator CI/CD pipeline succeeded 🎉</p>
        <ul>
          <li><b>Build #:</b> ${env.BUILD_NUMBER}</li>
          <li><b>Git Commit:</b> ${env.GIT_COMMIT}</li>
          <li><b>Docker Image:</b> ${env.IMAGE_TAG}</li>
        </ul>
        <p>Check your Docker Hub repo for the pushed image.</p>
        <p>– Jenkins CI/CD System</p>
        """,
        mimeType: 'text/html'
      )
    }
    failure {
      echo 'Pipeline failed'
      emailext (
        to: 'your_email@gmail.com',
        subject: "❌ FAILURE: Jenkins Build #${env.BUILD_NUMBER}",
        body: """
        <p>Hi Madhav,</p>
        <p>Your Scientific Calculator pipeline failed ⚠️</p>
        <p>Please check the Jenkins console output for details.</p>
        <p>– Jenkins CI/CD System</p>
        """,
        mimeType: 'text/html'
      )
    }
  }


} // end pipeline
