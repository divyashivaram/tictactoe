from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import create_or_join_game, get_all_games, index

# Create your views here.

urlpatterns = {
    path('', index, name="index"),
    path('allgames', get_all_games, name="items"),
    path('createUser', create_or_join_game, name="createUser")
}

urlpatterns = format_suffix_patterns(urlpatterns)
