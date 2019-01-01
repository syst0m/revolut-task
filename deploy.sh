#!/bin/bash

get_first_container_num() {
    echo `docker inspect --format='{{.Name}}' $(docker ps -q) | grep "$1" | awk -F  "_" '{print $NF}' | sort -r | head -1`
}

APP_FOLDER="revolut-task"
APP_NAME="api" # from docker-compose
APP_CONTAINER_NAME="$APP_FOLDER"_"$APP_NAME"

LB_NAME="load-balancer" # from docker-compose
LB_CONTAINER_NAME="$APP_FOLDER"_"$LB_NAME"

APP_CONTAINER_NUM=`get_first_container_num $APP_CONTAINER_NAME`
LB_CONTAINER_NUM=`get_first_container_num $LB_CONTAINER_NAME`

docker-compose build $APP_NAME
docker-compose scale $APP_NAME=2

printf "\nPreparing new container..."
sleep 5; # Allow container to fully start

printf "\nDraining traffic from old container"
docker exec -it "$LB_CONTAINER_NAME"_"$LB_CONTAINER_NUM" sh -c "echo set weight default_service/"$APP_CONTAINER_NAME"_"$APP_CONTAINER_NUM" 0 | socat stdio /var/run/haproxy.sock"

sleep 5; # Wait for connections to drain

printf "\nStopping container: "
docker stop "$APP_CONTAINER_NAME"_"$APP_CONTAINER_NUM"

printf "\nRemoving old container: "
docker rm "$APP_CONTAINER_NAME"_"$APP_CONTAINER_NUM"

printf "\nDone!"
