FROM mcr.microsoft.com/mlops/python:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY config.json config.json
COPY ./src /app/src
