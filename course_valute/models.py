import datetime

from django.db import models


class Valute(models.Model):
    country = models.CharField(max_length=100, verbose_name='Страна')
    country_code = models.CharField(max_length=100, verbose_name='Код')
    value = models.CharField(max_length=20, verbose_name='Курс')
    date_update = models.DateField(verbose_name='Дата обновления')

    objects = models.Manager()

    def __str__(self):
        return f'{self.country_code}'

    class Meta:
        ordering = ['country_code']
        indexes = [
            models.Index(fields=['country_code'])
        ]
