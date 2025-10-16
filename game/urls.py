from django.urls import path
from .views import NearbyBundlesAPIView, GameplayView, LeaderBoardView, SetCashableScoreView, settings_view, \
    selected_games_view

app_name = "game"
urlpatterns = [
    # version 1
    path("v1/bundles/nearby/", NearbyBundlesAPIView.as_view(), name="bundles-nearby"),

    # version 2
    path("v2/play/", GameplayView.as_view(), name="game-play"),
    path("v2/play/cashable", SetCashableScoreView.as_view(), name="cashable-score"),
    path("v2/leaderboard/", LeaderBoardView.as_view(), name="game-leaderboard"),
    path("v2/settings/", settings_view, name="game-settings"),
    path("v2/selected/", selected_games_view, name="game-selected"),
]
