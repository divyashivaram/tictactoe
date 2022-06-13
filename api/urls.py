from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import create_or_join_game, render_game, get_all_games, index, get_moves, update_moves


urlpatterns = {
    path('', index, name="index"),
    # TODO: Call this join_game and not createUser
    # TODO: Mixed cases here in names. Refactor
    path('createUser', create_or_join_game, name="createUser"),
    path(r'games/<slug:game_id>', render_game, name="get_game"),
    path('updateMoves', update_moves, name="updateMoves"),
    path('getmoves/<slug:game_id>', get_moves, name="getMoves"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
