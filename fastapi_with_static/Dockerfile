FROM python:3.11-slim-buster

RUN apt-get update -y && apt-get install -y build-essential libldap-dev libsasl2-dev

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt