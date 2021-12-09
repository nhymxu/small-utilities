# Stop every Docker container
docker stop $(docker ps -a -q)

# Delete every Docker container
docker rm $(docker ps -a -q)

# Delete every Docker image
docker rmi $(docker images -q)
