project = "gem-py"
team = "gem-py"

pipeline {
     environment {
           ARTIFACTORY = credentials("${project}-${team}-artifactory")
           // 3 environment variables will be automatically be defined: ARTIFACTORY (username:APIKey), ARTIFACTORY_USR (username) and ARTIFACTORY_PSW (APIKey)
     }
    agent {
        label 'agent-team'
    }
    stages {
        stage('Build') {
            steps {
                script {
                    if(BRANCH_NAME == "development") {
                        environment = "dev"
                    }else if(BRANCH_NAME == "release") {
                        environment = "uat"
                    }else if(BRANCH_NAME == "master") {
                        environment = "prod"
                    }else{
                        environment = "scratch"
                    }
                }
                sh 'python3.6 -m venv testenv'
                sh """
                . ./testenv/bin/activate
                python3.6 -m pip install --upgrade pip
                python3.6 -m pip install -e .[testing] --index https://${ARTIFACTORY}@artifactory.tools.digital.engie.com/artifactory/api/pypi/${project}-${team}-pypi-${environment}/simple --upgrade
                cd test
                nosetests . --exe --with-doctest --with-xunit --xunit-file python_unittest_out.xml --with-coverage --cover-erase --cover-package=../pycommon_test/. --cover-min-percentage=30 --cover-html
                coverage xml
                """
            }
        }
        stage('Deploy') {
            steps {
                sh 'python3.6 -m venv testenv'
                sh """ cat << EOF > .pypirc
[distutils]
index-servers=local
[local]
repository=https://artifactory.tools.digital.engie.com/artifactory/api/pypi/${project}-${team}-pypi-${environment}
username=${ARTIFACTORY_USR}
password=${ARTIFACTORY_PSW}
EOF
"""
                sh """
                . ./testenv/bin/activate
                python3.6 -m pip install --upgrade pip
                python3.6 -m pip install twine
                python3.6 setup.py sdist
                twine upload dist/* -r local --config-file ./.pypirc
                """
            }
        }
    }
}