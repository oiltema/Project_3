from django import forms

from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {'password': forms.PasswordInput()}


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise ValidationError('Имя пользователя занято')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise ValidationError('Емейл уже используется')
        return data

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароль не совпадает')
        return cd['password2']

    # def send_mail(self):
    #     sleep(20)
    #     profile = Profile.objects.filter(is_verified=False).last()
    #     send_email_confirm_registration(profile_pk=profile.pk)
        # subject = f"Подтверждение почты  для {profile.user.username}"
        # message = f'Для подтвреждения почты, перейдите по http://127.0.0.1:8000/user/register_success/{profile.auth_token}'
        # send_email_confirm_registration.apply_async(args=[subject, message, self.cleaned_data['email']])



class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'address', 'phone', 'image']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class PasswordChangeForm(forms.ModelForm):
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = User
        fields = ['password']
        widgets = {'password': forms.PasswordInput}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароль не совпадает')
        return cd['password2']