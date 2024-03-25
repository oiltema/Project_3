from django.urls import path

from .views import *

app_name = 'service'

urlpatterns = [
    path('', category_list, name='category_list'),
    path('category/<slug:category_slug>/', category_list, name='category_list_by_slug'),
    path('by_category/<slug:category_slug>/', performers_by_category, name='performers_by_category'),
    path('performer_create/', performer_create, name='performer_create'),
    path('performer_detail/<int:performer_pk>/', performer_detail, name='performer_detail'),
    path('review_delete!<int:review_pk>/', review_delete, name='review_delete'),
    path('mywork_delete!<int:mywork_pk>/', mywork_delete, name='mywork_delete'),
    path('type_work_delete!<int:type_work_pk>/', type_work_delete, name='type_work_delete'),
]