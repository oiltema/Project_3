from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        if request.user.pk is None:
            return redirect('user:login')
        if 'review_form' in request.POST:
            print('review_form')
            review_form = ReviewAddForm(request.POST)
            if review_form.is_valid():
                rf = review_form.save(commit=False)
                rf.user = request.user
                rf.performer = performer
                rf.save()
                return redirect('service:performer_detail', performer_pk)
        if 'my_works_form' in request.POST:
            print('my_works_form')
            my_works_form = MyWorkAddForm(request.POST, request.FILES)
            if my_works_form.is_valid():
                mw = my_works_form.save(commit=False)
                mw.performer = performer
                if len(mw.description.split(' ')) == 1:
                    messages.error(request, 'Неверно введено описание')
                    return redirect('service:performer_detail', performer_pk)
                mw.save()
                return redirect('service:performer_detail', performer_pk)
        if 'type_works_form' in request.POST:
            type_works_form = TypeWorkAddForm(request.POST)
            if type_works_form.is_valid():
                tw = type_works_form.save(commit=False)
                tw.performer = performer
                tw.save()
                return redirect('service:performer_detail', performer_pk)
    else:
        review_form = ReviewAddForm()
        my_works_form = MyWorkAddForm()
        type_works_form = TypeWorkAddForm()

    context = {
        'performer': performer,
        'reviews': reviews,
        'my_works': my_works,
        'type_works': type_works,
        'review_form': review_form,
        'my_works_form': my_works_form,
        'type_works_form': type_works_form
    }
    return render(request, 'service/performer_detail.html', context)


@login_required(login_url='user:login')
def performer_create(request):
    user = request.user
    if user.profile.first_name is None or user.profile.last_name is None:
        messages.error(request, 'Не заполнены поля профиля')
        return redirect('user:profile', user.username)
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


@login_required(login_url='user:login')
def review_delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    performer_pk = review.performer.pk
    review.delete()
    return redirect('service:performer_detail', performer_pk)


@login_required(login_url='user:login')
def mywork_delete(request, mywork_pk):
    mywork = MyWork.objects.get(pk=mywork_pk)
    performer_pk = mywork.performer.pk
    mywork.delete()
    return redirect('service:performer_detail', performer_pk)


@login_required(login_url='user:login')
def type_work_delete(request, type_work_pk):
    type_work = TypeWork.objects.get(pk=type_work_pk)
    performer_pk = type_work.performer.pk
    type_work.delete()
    return redirect('service:performer_detail', performer_pk)
