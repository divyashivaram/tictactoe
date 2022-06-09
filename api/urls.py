from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import create_or_join_game, create_item, get_all_games, manage_item, index

# Create your views here.

urlpatterns = {
    path('', index, name="index"),
    path('allgames', get_all_games, name="items"),
    path('createUser', create_or_join_game, name="createUser")
}

urlpatterns = format_suffix_patterns(urlpatterns)
