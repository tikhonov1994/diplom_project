from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from movies.models import UUIDMixin


class Template(UUIDMixin):
    name = models.CharField(max_length=64, unique=True)
    html_template = models.TextField()
    attributes = models.JSONField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "notification\".\"template"
        verbose_name = _('template')
        verbose_name_plural = _('templates')


class Mailing(UUIDMixin):
    class Statuses(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        IN_PROGRESS = 'IN_PROGRESS', _('In progress')
        DONE = 'DONE', _('Done')
        FAILED = 'FAILED', _('Failed')

    receiver_ids = ArrayField(models.UUIDField())
    status = models.CharField(max_length=50, choices=Statuses.choices, default=Statuses.CREATED,)
    subject = models.CharField(max_length=255)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    template_params = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notification\".\"mailing"
        verbose_name = _('mailing')
        verbose_name_plural = _('mailings')
