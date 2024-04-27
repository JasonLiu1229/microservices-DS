# syntax=docker/dockerfile:1
# Auth
FROM python:3.12-rc-slim-buster

WORKDIR /app/backend

COPY . /app/backend/

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app.backend:app", "--port", "8000", "--host", "0.0.0.0"]
