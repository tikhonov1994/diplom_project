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


# Для этой задачи предполагается наличие шаблона, который отрендерит список рецензий.
@shared_task(name='notify_new_popular_reviews')
def notify_new_popular_reviews(mailing_id: str, params: dict):
    mailing = Mailing.objects.get(id=UUID(mailing_id))

    reviews_response = requests.get('social_api:8010/social_api/api/v1/reviews/daily-top-reviews')
    reviews_response.raise_for_status()
    reviews: list[dict[str, any]] = reviews_response.json()

    data = {
        'template_id': mailing.template.pk,
        'template_params': params,
        'recipients_list': mailing.users_ids,
        'subject': params.get('subject')
    }

    for i in range(len(reviews)):
        film_response = requests.get(f'api:8001/content/api/v1/films/{reviews[i]["film_id"]}')
        film_response.raise_for_status()
        film_data = film_response.json()
        reviews[i]['film_title'] = film_data['title']

    data['template_params']['reviews'] = reviews
    requests.post('notification_api:8005/notification_api/api/v1/mailing/send', data=data)
