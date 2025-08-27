from django.contrib import admin

from game.models import Location, AssetBundle, GameHistory


# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(AssetBundle)
class AssetBundleAdmin(admin.ModelAdmin):
    pass


@admin.register(GameHistory)
class GameHistoryAdmin(admin.ModelAdmin):
    pass
