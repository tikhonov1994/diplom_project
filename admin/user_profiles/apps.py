from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profiles'

    verbose_name = _('user profiles')
