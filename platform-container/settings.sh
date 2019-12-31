#!/bin/bash

# The name of the docker image to produce
export IMAGE_NAME="taplatform"

# Extra packages to install
export EXTRA_PACKAGES=""
export EXTRA_DEVELOPMENT_PACKAGES=""

# Google Container Registry settings
# gcp-project-name-here
export GCR_PROJECT="mlproject01-207413"
export GCR_REGISTRY="${IMAGE_NAME}"
