pipeline {
  environment {
    registry = "messagebirdtemp/webapp"
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
    stage('Create Namespace'){
      steps{
        script{
          sh 'kubectl apply -f namespace-manifests/'
        }
      }
    }
    stage('Integration'){
      steps{
        script{
          //update deployment manifests with latest docker tag
          sh 'sed -i s,BUILD_ID,${BUILD_NUMBER},g deployment-manifests/integration/web-frontend-deployment.yaml'
          //deploy on cluster
          sh 'kubectl apply -f deployment-manifests/integration --namespace=webapp-integration'
          try{
           //Gathering ELB external IP address
           def ip = ''
           def count = 0
           def countLimit = 10

           //Waiting loop for IP address provisioning
           println("Waiting for IP address")
           while(ip=='' && count<countLimit) {
            //sleep while ELB being ready
            sleep 15
            ip = sh script: "kubectl get svc --namespace=webapp-integration -o jsonpath='{.items[*].status.loadBalancer.ingress[*].hostname}'", returnStdout: true
            ip=ip.trim()
            count++
           }

            if(ip==''){
              error("Not able to get the IP address. Aborting...")
            }
            else{
              //waiting till instance become healthly in the ELB
              sleep 120
              //Executing tests
              sh "chmod +x tests/integration_test.sh && ./tests/integration_test.sh ${ip}"

              //Cleaning the integration environment
              println("Cleaning integration environment...")
              sh 'kubectl delete -f deployment-manifests/integration --namespace=webapp-integration'
              println("Integration stage finished.")
            }

            }
            catch(Exception e) {
              println("Integration stage failed.")
              println("Cleaning integration environment...")
              sh 'kubectl delete -f deployment-manifests/integration --namespace=webapp-integration'
              error("Exiting...")
            }
          }
      }
    }
    stage('Production'){
      steps{
        script{
          //update deployment manifests with latest docker tag
          sleep 10
          sh 'sed -i s,BUILD_ID,${BUILD_NUMBER},g deployment-manifests/production/web-frontend-deployment.yaml'
          //deploy on cluster
          sh 'kubectl apply -f deployment-manifests/production --namespace=webapp-production'


          //Gathering ELB app's external IP address
             def ip = ''
             def count = 0
             def countLimit = 10

             //Waiting loop for IP address provisioning
             println("Waiting for IP address")
             while(ip=='' && count<countLimit) {
               //sleep while ELB being ready
               sleep 15
              ip = sh script: "kubectl get svc --namespace=webapp-production -o jsonpath='{.items[*].status.loadBalancer.ingress[*].hostname}'", returnStdout: true
              ip = ip.trim()
              count++
         }

       if(ip==''){
        error("Not able to get the IP address. Aborting...")

       }
       else{
         //waiting till instance become healthly in the ELB
         sleep 120
           //Executing tests

        sh "chmod +x tests/production_test.sh && ./tests/production_test.sh ${ip}"
              }
        }
      }
    }
  }
}
