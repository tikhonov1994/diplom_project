import os
import requests
from uuid import UUID

from django import setup

setup()

from celery import Celery, shared_task
from mailing.models import Mailing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')

app = Celery('tasks')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@shared_task(name='send_messages')
def send_messages(mailing_id: str, params: dict):
    mailing = Mailing.objects.get(id=UUID(mailing_id))
    data = {
        'template_id': mailing.template.pk,
        'template_params': params,
        'recipients_list': mailing.users_ids,
        'subject': None
    }
    requests.post('notification_api/notification_api/api/v1/mailing/send', data=data)
