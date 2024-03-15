from django.contrib import admin

from .models import Food, Comments


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created']
    list_filter = ['date_created']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['food', 'author', 'date_created']
    list_filter = ['food', 'date_created']
