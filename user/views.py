import uuid

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, RegisterForm, ProfileForm, UserEditForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from .tasks import send_email_confirm_registration


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user.profile.is_verified)
        if user is not None and user.profile.is_verified == True:
            login(request, user)
            return redirect('user:login')
        else:
            messages.error(request, 'Подтвердите электронную почту')
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/login_user.html', context)


@login_required(login_url='user:login')
def logout_user(request):
    logout(request)
    return redirect('user:login')


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.save()
            Profile.objects.create(user=new_user, auth_token=str(uuid.uuid4()))
            profile = Profile.objects.last()
            send_email_confirm_registration.apply_async(args=[profile.pk])
            # subject = f"Подтверждение почты для {profile.user.username}"
            # message = f'Для подтвреждения почты, перейдите по http://127.0.0.1:8000/user/register_success/{profile.auth_token}'
            # send_mail(subject, message, settings.EMAIL_HOST_USER, [form.cleaned_data.get('email')])
            return redirect('user:register_send_mail', profile.pk)

    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'user/register_user.html', context)


@login_required(login_url='user:login')
def profile_user(request, user_username):
    profile = Profile.objects.get(user__username=user_username)
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user:profile', profile.user.username)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserEditForm(instance=request.user)
    context = {
        'profile': profile,
        'profile_form': profile_form,
        'user_form': user_form
    }
    return render(request, 'user/profile_user.html', context)


@login_required(login_url='user:login')
def change_password(request, user_pk):
    user = User.objects.get(pk=user_pk)
    if request.method == 'POST':
        ch_pass = PasswordChangeForm(request.POST)
        if ch_pass.is_valid():
            form = ch_pass.save(commit=False)
            user.set_password(form.password)
            user.save()
            return redirect('user:profile', user.profile.user.pk)

    else:
        ch_pass = PasswordChangeForm()
    context = {
        'ch_pass': ch_pass
    }
    return render(request, 'user/change_password.html', context)


def register_send_mail(request, profile_pk):
    profile = Profile.objects.get(pk=profile_pk)
    context = {
        'profile': profile
    }
    return render(request, 'user/register_send_mail.html', context)


def register_success(request, user_token):
    profile = Profile.objects.get(auth_token=user_token)
    profile.is_verified = True
    profile.save()
    context = {
        'profile': profile
    }
    return render(request, 'user/register_success.html', context)