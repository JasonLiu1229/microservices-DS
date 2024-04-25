# syntax=docker/dockerfile:1
# User
FROM python:3.12-rc-slim-buster

WORKDIR /app/backend

COPY app_authentication.py app.py
COPY requirements.txt requirements.txt
COPY ./services/authentication.py service.py

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "backend.app:app", "--port", "8000", "--host", "0.0.0.0"]
