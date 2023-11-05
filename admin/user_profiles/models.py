from django.db import models
from movies.models import UUIDMixin

from django.utils.translation import gettext_lazy as _


class AvatarStatuses(models.TextChoices):
    WITHOUT = 'WITHOUT'
    ON_INSPECTION = 'ON_INSPECTION'
    ACCEPTED = 'ACCEPTED'
    NON_ACCEPTED = 'NON_ACCEPTED'


class UserProfile(UUIDMixin):
    time_zone = models.CharField('Time zone', max_length=12)
    phone_number = models.DecimalField('Phone number', max_digits=15, decimal_places=0)
    avatar_link = models.URLField('Avatar link', null=True, blank=True)
    avatar_status = models.CharField('Avatar status', max_length=28, choices=AvatarStatuses.choices,
                                     default=AvatarStatuses.WITHOUT)
    
    class Meta:
        db_table = "user\".\"user_profile"
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
