FROM python:3.10-slim

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /opt/app

COPY requirements.txt requirements.txt

RUN apt-get update && \
    pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["pytest", "."]
