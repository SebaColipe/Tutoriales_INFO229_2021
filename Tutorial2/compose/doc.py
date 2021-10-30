import os
os.system("docker rm -f $(docker ps -aq)")
os.system("docker images")

