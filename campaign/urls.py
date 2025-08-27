from django.urls import path
from .views import AddScoreView, LeaderboardView

app_name = 'campaign'
urlpatterns = [
    # version 1
    path('v1/score/add/', AddScoreView.as_view(), name='add-score'),
    path('v1/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),

    # version 2
]
