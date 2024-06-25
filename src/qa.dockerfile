FROM python:3.12-slim
USER root
WORKDIR /app
COPY . /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt