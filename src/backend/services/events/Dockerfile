# syntax=docker/dockerfile:1
# Auth
FROM python:3.12-rc-slim-buster

WORKDIR /app/backend

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
