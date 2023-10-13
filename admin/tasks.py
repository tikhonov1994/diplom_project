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


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, send_messages.s([Mailing.objects.first().pk,
#                                                     {'params': {'subject': 'hello'}}]),
#                                                     name='send every 10')


@shared_task(name='send_messages')
def send_messages(mailing_id: str, params: dict):
    mailing = Mailing.objects.get(id=UUID(mailing_id))
    data = {
        'template_id': mailing.template.pk,
        'template_params': params,
        'recipients_list': mailing.users_ids,
        'subject': params.get('subject')
    }
    requests.post('notification_api:8005/notification_api/api/v1/mailing/send', data=data)
