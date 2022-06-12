from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import create_or_join_game, render_game, get_all_games, index, get_moves, update_moves

# Create your views here.

urlpatterns = {
    path('', index, name="index"),
    path('allgames', get_all_games, name="items"),
    path(r'games/<slug:game_id>', render_game, name="get_game"),
    path('createUser', create_or_join_game, name="createUser"),
    path('getmoves/<slug:game_id>', get_moves, name="getMoves"),
    path('updateMoves', update_moves, name="updateMoves"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
