from django.urls import path

from .views import *

app_name = 'food'

urlpatterns = [
    path('', index, name='index'),
    path('detail/<slug:food_slug>/', food_detail, name='food_detail'),
    path('food_list?<int:tag_pk>/', food_list_by_tag, name='food_list_by_tag'),
    path('comment_delete/<int:comment_pk>/', comment_delete, name='comment_delete'),
]
