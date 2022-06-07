from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import create_item, manage_items, manage_item, index

# Create your views here.

urlpatterns = {
    path('', index, name="index"),
    path('items', manage_items, name="items"),
    path('item', create_item, name="item"),
    path('items/<slug:key>', manage_item, name="single_item"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
