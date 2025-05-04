from rest_framework import serializers
from .models import UserProgress


class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    campaign_name = serializers.CharField(source='campaign.name')

    class Meta:
        model = UserProgress
        fields = ['username', 'campaign_name', 'score']
