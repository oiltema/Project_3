from django.contrib import admin

from .models import Category, SubCategory, Performer, MyWork, TypeWork, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'phone', 'date_create']
    list_filter = ['user', 'category', 'date_create']
    search_fields = ['user', 'category']


@admin.register(MyWork)
class MyWorkAdmin(admin.ModelAdmin):
    list_display = ['performer', 'title', 'price']
    list_filter = ['performer']
    search_fields = ['performer', 'title']


@admin.register(TypeWork)
class TypeWorkAdmin(admin.ModelAdmin):
    list_display = ['performer', 'title', 'price']
    list_filter = ['performer']
    search_fields = ['performer', 'title']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'performer', 'date_create']
    list_filter = ['user', 'performer', 'date_create']
    search_fields = ['user', 'performer']


