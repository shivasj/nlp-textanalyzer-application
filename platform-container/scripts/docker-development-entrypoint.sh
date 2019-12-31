#!/bin/bash

set -e

if [ ! -f /.dockerenv ]; then
    echo "This script needs to run inside the Docker image"
    exit 1
fi

echo -en "\033[92m
The following commands are available:

    webserver
        Run a development web server accessible from http://127.0.0.1:9000/

    worker
        Run the Celery worker service and beat scheduler

    scheduler
        Run the Celery beat scheduler

    notebook
        Run jupyter notebook

\033[0m
"

webserver() {
    # Note: we force lifespan to on to work around this bug in Starlette:
    # https://github.com/encode/starlette/issues/486
    uvicorn api.service:app --reload --host 0.0.0.0 --port 9000 --lifespan on --log-level debug --reload-dir app "$@"
}

worker() {
    celery -A worker.service worker --loglevel=debug -B "$@"
}

scheduler() {
    celery -A worker.service beat --loglevel=info "$@"
}

notebook(){
    jupyter notebook --notebook-dir='notebooks' --ip 0.0.0.0 --no-browser --allow-root
}

export -f webserver
export -f worker
export -f scheduler
export -f notebook

# Load environment file
source environment.development

pipenv shell
