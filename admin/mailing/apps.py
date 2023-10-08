from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    verbose_name = _('mailing')
