from rest_framework import serializers
from .models import AssetBundle, Location


class AssetBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetBundle
        fields = ['id', 'name', 'file_url', 'start_time', 'end_time']


class LocationWithBundlesSerializer(serializers.ModelSerializer):
    bundles = AssetBundleSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'name', 'lat', 'lng', 'bundles']
