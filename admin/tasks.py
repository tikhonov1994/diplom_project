import os
from uuid import UUID
# from django.conf import settings

# settings.configure()

from django import setup
setup()

from mailing.models import Template, Mailing

from celery import Celery, shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')

app = Celery('tasks')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@shared_task(name='send_messages')
def send_messages(mailing_id: dict, params: dict):
    mailing = Mailing.objects.get(id=UUID(mailing_id.get('mailing_id')))
    return {
        'template': mailing.template.html_template,
        'params': params,
        'users_ids': mailing.users_ids
    }
