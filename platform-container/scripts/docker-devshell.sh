#!/bin/bash

# This script runs the docker image with the git repository bind-mounted to
# /app.

set -e

cleanup() {
    echo "cleaning up"
    docker-compose down
}

#pushd `git rev-parse --show-toplevel`

# Read the settings file
source ./settings.sh

# Ensure the image is up to date
./scripts/docker-build.sh

# Create the network if we don't have it yet
docker network inspect taplatform >/dev/null 2>&1 || docker network create taplatform

# Run the image and shut down the stack afterwards.
trap cleanup EXIT
docker-compose run --rm --service-ports --entrypoint="./scripts/docker-development-entrypoint.sh" --name $IMAGE_NAME app

#popd
