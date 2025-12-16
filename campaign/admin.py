from django.contrib import admin

from campaign.models import Campaign, CampaignLocation, UserProgress, WeeklyEvent, WeeklyUserScore


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


@admin.register(WeeklyEvent)
class WeeklyEventAdmin(admin.ModelAdmin):
    pass


@admin.register(WeeklyUserScore)
class WeeklyUserScoreAdmin(admin.ModelAdmin):
    pass
