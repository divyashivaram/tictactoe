from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import create_or_join_game, create_item, get_items, manage_item, index

# Create your views here.

urlpatterns = {
    path('', index, name="index"),
    path('items', get_items, name="items"),
    path('item', create_item, name="item"),
    path('items/<slug:key>', manage_item, name="single_item"),
    path('username', create_or_join_game, name="createUser")
}

urlpatterns = format_suffix_patterns(urlpatterns)
