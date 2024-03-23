from django.urls import path

from .views import *

app_name = 'food'

urlpatterns = [
    path('', index, name='index'),
    path('detail/<slug:food_slug>/', food_detail, name='food_detail'),
    path('food_list?<slug:category_slug>/', food_list_by_category, name='food_list_by_category'),
    path('comment_delete/<int:comment_pk>/', comment_delete, name='comment_delete'),
    path('add_like_<int:food_pk>/', add_like, name='add_like'),
    path('search/', search, name='search'),
    path('create/', food_create, name='food_create'),
    path('food_delete/<int:food_pk>/', food_delete, name='food_delete'),
    path('food_edit/<int:food_pk>/', food_edit, name='food_edit'),
]
