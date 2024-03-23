from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from pytils.translit import slugify


from .models import Food, Comments, Like, Category, SubCategory, StepFood

from .forms import CommentsForm, FoodAddForm, StepFoodAddForm


def index(request):
    foods = Food.objects.all()

    if request.method == 'POST':
        if request.POST.get('sort'):
            if request.POST.get('sort') == 'popular':
                foods = (Food.objects.all().annotate(like_count=Count('likes'), comments_count=Count('comments'))
                         .order_by('-like_count', '-views', '-comments_count'))
            else:
                foods = Food.objects.all().order_by(request.POST['sort'])

    # Пагинация
    paginator = Paginator(foods, 7)
    page_number = request.GET.get('page')
    foods = paginator.get_page(page_number)

    context = {
        'foods': foods
    }
    return render(request, 'food_site/index.html', context)


def food_detail(request, food_slug):
    food = get_object_or_404(Food, slug=food_slug)
    # Счетчик просмотров
    food.views += 1
    food.save()

    # Похожие рецепты
    # category_list = food.subcategory.values_list('pk', flat=True)
    # similar_foods = Food.objects.filter(subcategory__in=category_list).exclude(pk=food.pk).distinct()
    # similar_foods = similar_foods.annotate(subcategory_count=Count('subcategory')).order_by('-subcategory_count')[:7]

    steps = StepFood.objects.filter(food=food)

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
    else:
        comments_form = CommentsForm()

    context = {
        'food': food,
        'comments': comments,
        'comments_form': comments_form,
        'steps': steps,
    }
    return render(request, 'food_site/food_detail.html', context)


def food_list_by_category(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        foods = Food.objects.filter(subcategory__category=category)
    except:
        category = SubCategory.objects.get(slug=category_slug)
        foods = Food.objects.filter(subcategory=category)

    if request.method == 'POST':
        if request.POST['sort'] == 'popular':
            foods = Food.objects.filter(subcategory=category.pk).annotate(like_count=Count('likes'), comments_count=Count('comments')).order_by('-like_count', '-views', '-comments_count')
        else:
            foods = Food.objects.filter(subcategory=category.pk).order_by(request.POST['sort'], '-views')

    # Пагинация
    paginator = Paginator(foods, 7)
    page_number = request.GET.get('page')
    foods = paginator.get_page(page_number)

    context = {
        'category_name': category,
        'foods': foods
    }
    return render(request, 'food_site/food_list_by_category.html', context)


@login_required(login_url='user:login')
def comment_delete(request, comment_pk):
    comment = Comments.objects.get(pk=comment_pk)
    food = comment.food
    comment.delete()
    return redirect('food:food_detail', food.slug)


@login_required(login_url='user:login')
def add_like(request, food_pk):
    food = get_object_or_404(Food, pk=food_pk)
    try:
        like = Like.objects.get(food=food, user=request.user)
        like.delete()

    except ObjectDoesNotExist:
        Like.objects.create(food=food, user=request.user)

    return redirect('food:food_detail', food.slug)


def search(request):
    if request.method == 'POST':
        if request.POST.get('search') != '':
            search_item = request.POST.get('search')
            foods = Food.objects.filter(Q(title__icontains=search_item.title()) |
                                        Q(description__icontains=search_item))

            paginator = Paginator(foods, 7)
            page_number = request.GET.get('page')
            foods = paginator.get_page(page_number)

            context = {
                'foods': foods,
                'search_item': search_item
            }
            return render(request, 'food_site/search.html', context)

        else:
            return redirect('food:index')


@login_required(login_url='user:login')
def food_create(request):
    if request.method == 'POST':
        food_form = FoodAddForm(request.POST, request.FILES)
        if food_form.is_valid():
            ff = food_form.save(commit=False)
            ff.author = request.user
            ff.slug = slugify(food_form.cleaned_data['title'])
            ff.save()
            return redirect('food:food_detail', ff.slug)
    else:
        food_form = FoodAddForm()
    context = {
        'food_form': food_form
    }
    return render(request, 'food_site/food_create.html', context)


def food_delete(request, food_pk):
    food = Food.objects.get(pk=food_pk)
    if request.user.username == food.author.username:
        food.delete()
    return redirect('food:index')


def food_edit(request, food_pk):
    food = Food.objects.get(pk=food_pk)
    if request.method == 'POST':
        food_form = FoodAddForm(instance=food, data=request.POST, files=request.FILES)
        step_form = StepFoodAddForm(request.POST, request.FILES)
        print(food_form.is_valid() and step_form.is_valid())
        if food_form.is_valid():
            ff = food_form.save(commit=False)
            ff.save()
            return redirect('food:food_detail', food.slug)

        if step_form.is_valid():
            sf = step_form.save(commit=False)
            sf.food = food
            sf.save()
            return redirect('food:food_edit', food.pk)
    else:
        food_form = FoodAddForm(instance=food)
        step_form = StepFoodAddForm()

    steps = StepFood.objects.filter(food=food)

    context = {
        'food_form': food_form,
        'step_form': step_form,
        'steps': steps
    }
    return render(request, 'food_site/food_edit.html', context)

