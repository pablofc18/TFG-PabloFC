pipeline {
    agent any

    stages {
        stage('Stop Flask') {
            steps {
                sshagent(credentials: ['ssh-vm1-app']) {
                    script {
                        try {
                            sh """
                                ssh -o StrictHostKeyChecking=no pablofc18@192.168.1.10 "
                                    cd myApp/APPWITHFLASK
                                    pwd
                                    sudo systemctl stop appFlask.service
                                    exit
                                "
                            """
                            echo "Stopped successfully"
                        } catch (Exception e) {
                            echo "Error in ssh connection: ${e.getMessage()}"
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "I finished!"
        }
        success {
            echo "Im okey :D"
        }
    }
}