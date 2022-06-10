from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import create_or_join_game, render_game, get_all_games, index

# Create your views here.

urlpatterns = {
    path('', index, name="index"),
    path('allgames', get_all_games, name="items"),
    path('games/<slug:game_id>', render_game, name="get_game"),
    path('createUser', create_or_join_game, name="createUser")
    # path('users', create_or_join_game, name="createUser"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
