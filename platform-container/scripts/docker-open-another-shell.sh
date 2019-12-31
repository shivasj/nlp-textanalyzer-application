#!/bin/bash

if [ -f /.dockerenv ]; then
    echo "This script needs to run outside of the Docker image"
    exit 1
fi

docker ps | grep "\<taplatform\>" | awk '{print $1}' | xargs -o -I CONTAINER_ID docker exec -ti CONTAINER_ID scripts/docker-development-entrypoint.sh
