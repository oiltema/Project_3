from django.contrib import admin

from .models import Valute


@admin.register(Valute)
class ValuteAdmin(admin.ModelAdmin):
    list_display = ['country', 'country_code', 'value', 'date_update']
