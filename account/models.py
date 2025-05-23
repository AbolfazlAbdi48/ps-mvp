from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name=_('Nick Name'))

    def __str__(self):
        return self.get_username()


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"

    @staticmethod
    def generate_code():
        return str(random.randint(1000, 9999))
