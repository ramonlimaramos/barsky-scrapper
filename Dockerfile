FROM python:3.8

WORKDIR /usr/src/app
ENV PYTHONPATH /usr/src/app
ENV PYTHONUNBUFFERED 1

# Project Setup
RUN apt-get update -y && apt-get upgrade -y && apt-get install librabbitmq-dev libmemcached-dev libxml2-dev libxmlsec1-dev libxmlsec1-openssl -y

# Docker requirements
COPY requirements_docker.txt requirements_docker.txt
RUN pip install --upgrade pip && pip install -r requirements_docker.txt

# Requirements
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY extras/scripts/entrypoint.sh extras/scripts/entrypoint.sh
RUN chmod 775 extras/scripts/entrypoint.sh && chmod u+s extras/scripts/entrypoint.sh

# Project files
USER 1000
COPY setup.py setup.py
COPY README.md README.md
COPY alembic.ini alembic.ini
COPY barsky_scrapper barsky_scrapper

# Run app
ENTRYPOINT ["extras/scripts/entrypoint.sh"]
