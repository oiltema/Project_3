from django.shortcuts import render, redirect

from .models import Food
from taggit.models import Tag


def get_all_tags(request):
    tag_list = ['Суп', 'Второе', 'Закуска']
    tags = Tag.objects.all().exclude(name__in=tag_list)
    tags_main = Tag.objects.filter(name__in=tag_list)
    return {'tags_main': tags_main, 'tags_all': tags}


def get_all_foods(request):
    foods_all = Food.objects.all()
    if request.method == 'POST':
        foods_all = Food.objects.all().order_by(request.POST['sort'])
    return {'foods_all': foods_all}