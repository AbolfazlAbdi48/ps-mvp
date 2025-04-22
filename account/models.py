from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name=_('Nick Name'))

    def __str__(self):
        return self.get_username()
