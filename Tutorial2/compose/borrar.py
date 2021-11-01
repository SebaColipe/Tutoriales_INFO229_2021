from os import system as s
s("docker rm -f $(docker ps -aq)")
s("docker rmi -f compose_app:latest")
s("docker-compose down")
s("docker-compose rm")
s("docker volume prune")
#s("docker-compose up")