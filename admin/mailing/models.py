from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from movies.models import UUIDMixin


class Template(UUIDMixin):
    name = models.CharField(max_length=64)
    html_template = models.TextField()
    attributes = models.JSONField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('template')
        verbose_name_plural = _('templates')


class Mailing(UUIDMixin):
    users_ids = ArrayField(models.UUIDField())
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('mailing')
        verbose_name_plural = _('mailings')
