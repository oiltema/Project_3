from django.db import models
from django.conf import settings
from PIL import Image

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Фамилия')
    city = models.CharField(max_length=25, blank=True, null=True, verbose_name='Город')
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Адрес')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер')
    image = models.ImageField(upload_to='user/%Y/%m/%d', default='img/user.png', blank=True, null=True,)

    created = models.DateTimeField(auto_now_add=True)
    auth_token = models.CharField(max_length=100, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}, {self.city}'

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)