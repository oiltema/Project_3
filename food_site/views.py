from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.db.models import Count
from django.urls import reverse


from taggit.models import Tag
from .models import Food, Comments

from .forms import CommentsForm


def index(request):

    return render(request, 'food_site/index.html')


def food_detail(request, food_slug):
    food = get_object_or_404(Food, slug=food_slug)

    # Похожие рецепты
    tags_list = food.tags.values_list('pk', flat=True)
    similar_foods = Food.objects.filter(tags__in=tags_list).exclude(pk=food.pk).distinct()
    similar_foods = similar_foods.annotate(tag_count=Count('tags')).order_by('-tag_count')[:7]

    # Комментарии
    comments = Comments.objects.filter(food=food)
    if request.method == 'POST':
        comments_form = CommentsForm(request.POST)
        if comments_form.is_valid():
            cf = comments_form.save(commit=False)
            cf.food = food
            cf.author = request.user
            cf.save()
            return redirect('food:food_detail', food.slug)
            # return redirect(reverse('food:food_detail', food.slug) + '#comments')
    else:
        comments_form = CommentsForm()
    context = {
        'food': food,
        'similar_foods': similar_foods,
        'comments': comments,
        'comments_form': comments_form
    }
    return render(request, 'food_site/food_detail.html', context)


def food_list_by_tag(request, tag_pk):
    tag = get_object_or_404(Tag, pk=tag_pk)
    foods = Food.objects.filter(tags=tag.pk)
    context = {
        'tag': tag,
        'foods': foods
    }
    return render(request, 'food_site/food_list_by_tag.html', context)


def comment_delete(request, comment_pk):
    comment = Comments.objects.get(pk=comment_pk)
    food = comment.food
    comment.delete()
    return redirect('food:food_detail', food.slug)
