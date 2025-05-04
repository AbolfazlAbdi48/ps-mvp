from django.urls import path
from .views import AddScoreView, LeaderboardView

app_name = 'campaign'
urlpatterns = [
    path('score/add/', AddScoreView.as_view(), name='add-score'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
