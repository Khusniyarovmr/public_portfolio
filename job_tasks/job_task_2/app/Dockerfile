FROM python:3.11
RUN apt-get update -y && apt-get install -y python3-pip python-dev build-essential
RUN pip install --upgrade pip
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src
COPY ./wait_for_it.sh ./wait_for_it.sh
RUN chmod +x ./wait_for_it.sh
