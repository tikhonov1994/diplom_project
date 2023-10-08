import os
from uuid import UUID

from django import setup
from celery import Celery, shared_task

from mailing.models import Mailing

setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')

app = Celery('tasks')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@shared_task(name='send_messages')
def send_messages(mailing_id: str, params: dict):
    mailing = Mailing.objects.get(id=UUID(mailing_id))
    return {
        'template': mailing.template.html_template,
        'params': params,
        'users_ids': mailing.users_ids
    }
