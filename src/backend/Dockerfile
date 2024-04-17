# syntax=docker/dockerfile:1
FROM python:3.12-rc-slim-buster

WORKDIR /app/backend

COPY app.py app.py
COPY requirements.txt requirements.txt
COPY /services /services

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=127.0.0.1 --port=8000 &", "--no-reload"]
