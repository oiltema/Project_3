from django.urls import path

from .views import *

app_name = 'user'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register_user/', register_user, name='register'),
    path('profile_user/<str:user_username>', profile_user, name='profile'),
    path('change_password/<int:user_pk>', change_password, name='change_password'),
    path('register_send_mail/<int:profile_pk>', register_send_mail, name='register_send_mail'),
    path('register_success/<str:user_token>', register_success, name='register_success')
]