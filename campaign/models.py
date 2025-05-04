from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User
from game.models import Location, AssetBundle


# Create your models here.
class Campaign(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    reward_type = models.CharField(
        max_length=10,
        choices=[('instant', 'لحظه‌ای'), ('collective', 'تجمیعی')],
        verbose_name=_('Reward Type')
    )
    reward_amount = models.PositiveIntegerField(default=10, verbose_name=_('Reward Amount'))

    class Meta:
        verbose_name = _('Campaign')
        verbose_name_plural = _('1. Campaigns')

    def __str__(self):
        return self.name


class CampaignLocation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='locations',
                                 verbose_name=_('Campaign'))
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name=_('Location'))

    class Meta:
        verbose_name = _('Campaign Location')
        verbose_name_plural = _('2. Campaign Locations')

    def __str__(self):
        return f"{self.campaign.name} - {self.location.name}"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name=_('Campaign'))
    scanned_bundles = models.ManyToManyField(AssetBundle, null=True, verbose_name=_('Scanned Bundles'))
    score = models.PositiveIntegerField(default=0, verbose_name=_('Score'))
    is_rewarded = models.BooleanField(default=False, verbose_name=_('Rewarded'))  # for collective challenges
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('User Progress')
        verbose_name_plural = _('3. User Progresses')

    # TODO: rewards model

    def __str__(self):
        return f"{self.user} - {self.campaign.name}"
