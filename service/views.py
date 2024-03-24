from django.shortcuts import render, redirect

from .models import Category, SubCategory, Performer, TypeWork, MyWork, Review
from .forms import PerformerCreateForm, MyWorkAddForm, TypeWorkAddForm, ReviewAddForm


def category_list(request, category_slug=None):
    category = Category.objects.all()
    subcategory = SubCategory.objects.filter(category=category.first())

    get_cat = None

    if category_slug:
        get_cat = Category.objects.get(slug=category_slug)
        subcategory = SubCategory.objects.filter(category__in=[get_cat])

    context = {
        'category': category,
        'subcategory': subcategory,
        'get_cat': get_cat,
    }
    return render(request, 'service/category_list.html', context)


def performers_by_category(request, category_slug):
    performers = Performer.objects.filter(category__slug=category_slug)
    context = {
        'performers': performers
    }
    return render(request, 'service/performers_by_category.html', context)


def performer_detail(request, performer_pk):
    performer = Performer.objects.get(pk=performer_pk)
    reviews = Review.objects.filter(performer=performer)
    my_works = MyWork.objects.filter(performer=performer)
    type_works = TypeWork.objects.filter(performer=performer)

    if request.method == 'POST':
        review_form = ReviewAddForm(request.POST)
        if review_form.is_valid():
            rf = review_form.save(commit=False)
            rf.user = request.user
            rf.performer = performer
            rf.save()
            return redirect('service:performer_detail', performer_pk)
    else:
        review_form = ReviewAddForm()
    context = {
        'performer': performer,
        'reviews': reviews,
        'my_works': my_works,
        'type_works': type_works,
        'review_form': review_form,
    }
    return render(request, 'service/performer_detail.html', context)


def performer_create(request):
    if request.method == 'POST':
        performer_create_form = PerformerCreateForm(request.POST)
        if performer_create_form.is_valid():
            per = performer_create_form.save(commit=False)
            per.user = request.user
            per.save()
            return redirect('service:performer_detail', per.pk)
    else:
        performer_create_form = PerformerCreateForm()

    context = {
        'performer_create_form': performer_create_form
    }
    return render(request, 'service/performer_create.html', context)

