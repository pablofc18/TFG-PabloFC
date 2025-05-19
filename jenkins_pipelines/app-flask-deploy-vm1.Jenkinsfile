pipeline {
    agent any

    stages {
        stage('Deploy Flask') {
            steps {
                sshagent(credentials: ['ssh-vm1-app']) {
                    script {
                        try {
                            sh """
                                ssh -o StrictHostKeyChecking=no pablofc18@192.168.1.10 "
                                    cd myApp/APPWITHFLASK
                                    pwd
                                    git pull
                                    if ! docker ps --format "{{.Names}}" | grep -q "^postgres_db\$"; then
                                        echo "Container postgres_db not running. Starting it..."
                                        docker start postgres_db
                                    else
                                        echo "Container postgres_db already executing."
                                    fi
                                    sudo systemctl restart appFlask.service
                                    exit
                                "
                            """
                            echo "Deploy succeded"
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