FROM python:3.10-slim

WORKDIR /opt/schemas

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]