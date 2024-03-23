from django.shortcuts import render, redirect
from django.db.models import Count

from .models import Food, Category, SubCategory


def get_all_category(request):
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    return {'category': category, 'subcategory': subcategory}


def get_popular_foods(request):
    foods = Food.objects.annotate(like_count=Count('likes')).order_by('-like_count', 'views')[:5]
    return {'food_popular': foods}