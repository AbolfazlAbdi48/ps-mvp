from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    lat = models.FloatField(verbose_name=_("Lat"))
    lng = models.FloatField(verbose_name=_("Long"))
    alt = models.FloatField(blank=True, null=True, verbose_name=_("alt"))

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('2. Locations')

    def __str__(self):
        return self.name


class AssetBundle(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    file_url = models.URLField(verbose_name=_("File"))
    start_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Start"))
    end_time = models.DateTimeField(null=True, blank=True, verbose_name=_("End"))
    locations = models.ManyToManyField(Location, related_name='bundles', verbose_name=_("Locations"))
    points_per_tap = models.IntegerField(default=10, verbose_name=_("Points per Tap"))
    required_score_to_show = models.IntegerField(default=0, verbose_name=_("Required Score to show"))

    class Meta:
        verbose_name = _('Asset Bundle')
        verbose_name_plural = _('1. Asset Bundles')

    def __str__(self):
        return self.name


class GameHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_start_time = models.DateTimeField(auto_now_add=True)
    session_end_time = models.DateTimeField(null=True, blank=True)
    score_gained = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Game History')
        verbose_name_plural = _('3. Game Histories')

    def __str__(self):
        return f'{self.user.username} - {self.session_start_time.strftime("%Y-%m-%d %H:%M")}'
