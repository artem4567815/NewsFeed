FROM python:3.12-alpine3.21

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir gunicorn

RUN apk add --no-cache curl

COPY . .