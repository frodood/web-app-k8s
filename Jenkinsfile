pipeline {
  environment {
    registry = "frodood/webapp"
    registryCredential = "dockerhub"
    dockerImage = 'webapp'
  }
  agent any
  stages {
    stage('Cloning Git') {
      steps {
        git 'https://github.com/frodood/web-app-k8s.git'
      }
    }
  stage('Building image') {
      steps{
        script {
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
        }
      }
    }
    stage('Deploy Image') {
      steps{
         script {
            docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
    stage('Integration'){
      steps{
        script{
          sh 'kubectl apply -f deployment-manifests/'
          try{
           //Gathering python app's external IP address
           def ip = ''
           def count = 0
           def countLimit = 10

           //Waiting loop for IP address provisioning
           println("Waiting for IP address")
           while(ip=='' && count<countLimit) {
            sleep 30
            ip = sh script: "kubectl get svc -o jsonpath='{.items[*].status.loadBalancer.ingress[*].hostname}'", returnStdout: true
            ip=ip.trim()
            count++
           }

     if(ip==''){
      error("Not able to get the IP address. Aborting...")
         }
     else{
                 //Executing tests
                 sleep 120
      sh "chmod +x tests/integration_test.sh && ./tests/integration_test.sh ${ip}"

      //Cleaning the integration environment
      println("Cleaning integration environment...")
      sh 'kubectl delete -f deployment-manifests'
          println("Integration stage finished.")
     }

          }
     catch(Exception e) {
      println("Integration stage failed.")
       println("Cleaning integration environment...")
       sh 'kubectl delete -f deployment-manifests'
           error("Exiting...")
          }
        }
      }
    }

  }
}
