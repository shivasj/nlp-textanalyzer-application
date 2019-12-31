set -e

if [ ! -f /.dockerenv ]; then
    echo "This script needs to run inside the Docker image"
    exit 1
fi

# Note: we force lifespan to on to work around this bug in Starlette:
# https://github.com/encode/starlette/issues/486
pipenv run uvicorn api.service:app --host 0.0.0.0 --port 9000 --lifespan on
