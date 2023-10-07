FROM python:3.10-slim

WORKDIR /opt/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python", "tasks.py"]

