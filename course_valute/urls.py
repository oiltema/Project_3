from django.urls import path, include

from .views import *

app_name = 'course'

urlpatterns = [
    path('', valute_list, name='valute_list')
]