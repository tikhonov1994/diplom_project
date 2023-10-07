FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'example.settings'

# Скопируйте в контейнер файлы, которые редко меняются
COPY run_uwsgi.sh run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  apt-get update && apt-get install -y gettext \
     && mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir \
     && pip install python-dateutil \
     && pip install requests

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла.
COPY . .

# Порт, на котором приложение будет доступно внутри Docker-сети
EXPOSE 8000

RUN ["chmod", "+x", "run_uwsgi.sh"]

ENTRYPOINT [ "./run_uwsgi.sh"]
CMD celery -A tasks beat -l info -S django