FROM python:3.10-slim

WORKDIR /opt/app

EXPOSE 8002

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt

RUN  apt-get update && apt-get install \
     && pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir \
     && pip install python-dateutil

COPY . .

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT [ "./entrypoint.sh"]