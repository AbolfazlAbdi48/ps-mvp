from django.contrib import admin

from campaign.models import Campaign, CampaignLocation, UserProgress


# Register your models here.
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass


@admin.register(CampaignLocation)
class CampaignLocationAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    pass
