from time import sleep
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

from .models import Profile


@shared_task()
def send_email_confirm_registration(profile_pk):
    sleep(10)
    profile = Profile.objects.get(pk=profile_pk)
    subject = f'Подтверждение почты для {profile.user.username}'
    message = f'Для завершения регистрации перейдите по http://127.0.0.1:8000/user/register_success/{profile.auth_token}'
    ready = send_mail(subject, message, settings.EMAIL_HOST_USER, [profile.user.email], fail_silently=False)
    return ready
