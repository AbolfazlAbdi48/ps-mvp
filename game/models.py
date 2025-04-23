from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    lat = models.FloatField(verbose_name=_("Lat"))
    lng = models.FloatField(verbose_name=_("Long"))
    alt = models.FloatField(blank=True, null=True, verbose_name=_("alt"))

    def __str__(self):
        return self.name


class AssetBundle(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    file_url = models.URLField(verbose_name=_("File"))
    start_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Start"))
    end_time = models.DateTimeField(null=True, blank=True, verbose_name=_("End"))
    locations = models.ManyToManyField(Location, related_name='bundles', verbose_name=_("Locations"))

    def __str__(self):
        return self.name
