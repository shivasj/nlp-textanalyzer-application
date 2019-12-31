#!/bin/bash

# This script builds a new version of the docker image. Can be executed from
# anywhere within the repository.
#
# Note: the script automatically pushes production builds to GCR. Before you
# can do so you need to run "gcloud auth configure-docker" on your development
# machine. This only needs to be done once.

set -e

#pushd `git rev-parse --show-toplevel`

# Load settings
source ./settings.sh

DEVELOPMENT=1
FORCE=0

while getopts "hpf" arg; do
    case "${arg}" in
        h)
            echo "usage: $0 [options]"
            echo
            echo "options:"
            echo "    -p: build production image"
            echo "    -f: force a full rebuild without layer caching"
            exit 1
            ;;
        p)
            DEVELOPMENT=0
            ;;
        f)
            FORCE=1
            ;;
    esac
done

if [ "$DEVELOPMENT" -ne 0 ]; then
    DOCKER_ARGS=( --build-arg EXTRA_PACKAGES="${EXTRA_DEVELOPMENT_PACKAGES} ${EXTRA_PACKAGES}" --build-arg PIPENV_ARGS="--dev" )
else
    DOCKER_ARGS=( --build-arg EXTRA_PACKAGES="${EXTRA_PACKAGES}" )
fi

if [ "$FORCE" -ne 0 ]; then
    DOCKER_ARGS+=( --no-cache )
fi

# Build the docker image
docker build "${DOCKER_ARGS[@]}" -t ${IMAGE_NAME} -f Dockerfile .

# Push to GCR if we are building a production image
if [ "$DEVELOPMENT" -eq 0 ]; then
    TAG=`git rev-parse --short HEAD`

    docker tag ${IMAGE_NAME} gcr.io/${GCR_PROJECT}/${GCR_REGISTRY}:${TAG}
    docker push gcr.io/${GCR_PROJECT}/${GCR_REGISTRY}:${TAG}
fi

#popd
