pipeline {
  agent none
  stages{
    stage('Checkout, Test & Build'){
      agent { 
      docker { 
        image 'python:3.7.2' 
        args '-p 3001:3000'
      } 
      } 
      environment {
        HOME = '.'
      }
      stages {
        stage('Install') {
          steps {
            sh 'pip3 install -r requirements.txt'
          }
        }
      }
    }
    stage('Deploy'){
      agent{
        label 'master'
      }
      options{
        skipDefaultCheckout()
      }
      steps {
        sh 'rm -rf /var/www/monitoreo'
        sh 'mkdir /var/www/monitoreo'
        sh 'cp -Rp src /var/www/fedent'
        sh 'docker stop monitoreo || true && docker rm monitoreo || true'
        sh 'docker run -dit --name monitoreo -p 8002:80 -v /var/www/monitoreo/:/usr/local/apache2/htdocs/ httpd:2.4'
        echo "deploying the application"
      }
    }
  }
}