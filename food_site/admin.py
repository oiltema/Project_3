from django.contrib import admin

from .models import Food, Comments, Like, Category, SubCategory, StepFood


class LikeInLine(admin.TabularInline):
    model = Like
    raw_id_fields = ['food']


class StepsInLine(admin.StackedInline):
    model = StepFood
    raw_id_fields = ['food']

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'views', 'date_created']
    list_filter = ['date_created']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title', )}
    inlines = [LikeInLine, StepsInLine]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['food', 'author', 'date_created']
    list_filter = ['food', 'date_created']
    search_fields = ['food', 'author']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['food', 'user', 'like']
    list_filter = ['food']
    search_fields = ['food']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    list_filter = ['title', 'category']
    search_fields = ['title', 'category']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(StepFood)
class StepFoodAdmin(admin.ModelAdmin):
    list_display = ['food', 'text']
    search_fields = ['food']
    list_filter = ['food']
