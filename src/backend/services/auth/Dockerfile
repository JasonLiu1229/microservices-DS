# syntax=docker/dockerfile:1
# Auth
FROM python:3.12-rc-slim-buster

WORKDIR /app/backend

COPY . /app/backend/

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app:app","--proxy-headers", "--host", "127.0.0.1", "--port", "8000"]
