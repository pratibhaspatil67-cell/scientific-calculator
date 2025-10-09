pipeline {
  agent any
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
      echo '✅ Pipeline succeeded!'
      emailext (
        to: 'madhavspatil07@gmail.com',
        subject: "✅ SUCCESS: Jenkins Build #${env.BUILD_NUMBER}",
        body: """
        <h3>🎉 Jenkins Pipeline Success!</h3>
        <p>Your Scientific Calculator CI/CD pipeline completed successfully.</p>
        <ul>
          <li><b>Build #:</b> ${env.BUILD_NUMBER}</li>
          <li><b>Git Commit:</b> ${env.GIT_COMMIT}</li>
          <li><b>Docker Image:</b> ${env.IMAGE_TAG}</li>
        </ul>
        <p>The image has been pushed to Docker Hub and deployed via Ansible.</p>
        <p>– Jenkins Automated System</p>
        """,
        mimeType: 'text/html'
      )
    }

    failure { 
      echo '❌ Pipeline failed!'
      emailext (
        to: 'madhavspatil07@gmail.com',
        subject: "❌ FAILURE: Jenkins Build #${env.BUILD_NUMBER}",
        body: """
        <h3>⚠️ Jenkins Pipeline Failed!</h3>
        <p>Your Scientific Calculator CI/CD pipeline failed.</p>
        <p>Check Jenkins console logs for details.</p>
        <p>– Jenkins Automated System</p>
        """,
        mimeType: 'text/html'
      )
    }
  }
}
