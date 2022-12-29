#!/bin/bash
export CONTAINER_PORT=8080
export WORLD_PORT=8080
export WORLD_IP="0.0.0.0"
export IMAGE_HUB_NAME="boomland/csgo_fastapi:v1"

#
# docker build -f Dockerfile -t csgo_fastapi . 

docker pull $IMAGE_HUB_NAME
docker run -p "$CONTAINER_PORT:$WORLD_PORT" -e PORT=$CONTAINER_PORT -e IP=$WORLD_IP -d $IMAGE_HUB_NAME