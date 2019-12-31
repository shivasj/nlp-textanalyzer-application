# Use the official Debian-hosted Python image
FROM python:3.6.8-slim-stretch

ARG EXTRA_PACKAGES=""
ARG PIPENV_ARGS=""

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Tell pipenv where the shell is. This allows us to use "pipenv shell" as a
# container entry point.
ENV PYENV_SHELL=/bin/bash

# Ensure we have an up to date baseline, install dependencies and create a user
# so we don't run the app as root.
RUN set -ex; \
    for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential $EXTRA_PACKAGES && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    useradd -ms /bin/bash app -d /home/app -G sudo -u 1000 -p "$(openssl passwd -1 taplatform)" && \
    mkdir -p /app && \
    chown app:app /app && \
    echo "%sudo ALL=(ALL) NOPASSWD: /usr/local/bin/pip" >> /etc/sudoers

EXPOSE 8000

# Switch to the new user
USER app
WORKDIR /app

# Install python packages
ADD --chown=app:app Pipfile Pipfile.lock /app/
RUN pipenv sync $PIPENV_ARGS

# SPACY Download en
RUN pipenv run python -m spacy download en

# Jupyter notebook
#RUN pipenv run python -m ipykernel install --user --name=taplatform

# Add the rest of the source code. This is done last so we don't invalidate all
# layers when we change a line of code.
ADD --chown=app:app . /app

ENTRYPOINT ["./scripts/docker-production-entrypoint.sh"]
