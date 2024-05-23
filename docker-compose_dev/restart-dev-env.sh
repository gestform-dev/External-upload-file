#!/bin/bash

#To delete all containers:
docker rm -f $(docker ps -aq)

# To delete all containers including its volumes use,
#docker rm -vf $(docker ps -aq)

# Remove all volumes
#docker volume rm $(docker volume ls -q)

#To delete all the images
docker rmi -f $(docker images -aq)

#This will pull the image
#docker-compose pull

# to build the image instead of pulling it
docker-compose -f docker-compose-dev.yml build --no-cache

# To be able to login, you will need a super user. To create it, execute the following command:
#docker-compose -f docker-compose-dev.yml run --rm webserver createsuperuser

# This will create and start the necessary containers.
docker-compose -f docker-compose-dev.yml up

# Run django server on debug mode
#docker exec paperless_webserver_1 python3 manage.py runserver 0.0.0.0:8080