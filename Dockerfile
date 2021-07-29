# syntax=docker/dockerfile:1
# The first line to add to the Dockerfile is a # syntax parser directive. While optional, this directive instructs the Docker builder what syntax to use when parsing the Dockerfile, and allows older Docker versions with BuildKit enabled to upgrade the parser before starting the build. Parser directives must appear before any other comment, whitespace, or Dockerfile instruction in your Dockerfile, should be the first line in Dockerfiles.

FROM python:3.8-slim-buster

WORKDIR /mlops

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]