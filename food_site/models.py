from django.db import models
from PIL import Image
from django.urls import reverse
from pytils.translit import slugify

from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Слаг')

    objects = models.Manager()

    class Meta:
        ordering = ['pk']
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory', verbose_name='Категория')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Слаг')

    objects = models.Manager()

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title


class Food(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, related_name='subcategory', verbose_name='Субкатегория')
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=150, verbose_name='Слаг')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=User, related_name='food', verbose_name='Автор')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    time_cook = models.PositiveIntegerField(default=0, verbose_name='Время готовки')
    portion = models.PositiveIntegerField(default=1, verbose_name='Порций')
    products = models.TextField(max_length=2000, verbose_name='Продукты')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(upload_to=f'food/%Y/%m', blank=True, null=True, verbose_name='Изображение')

    views = models.PositiveIntegerField(default=0, verbose_name='Просмотров')

    objects = models.Manager()

    class Meta:
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created'])
        ]

    def __str__(self):
        return f'{self.title}, {self.author}, {self.date_created}'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        if not self.slug:
            self.slug = slugify(self.slug)
            super().save()

    def get_absolute_url(self):
        return reverse('food:food_detail', args=[self.slug])


class Comments(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='comments', verbose_name='Рецепт')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments', verbose_name='Автор')
    text = models.TextField(max_length=2000, verbose_name='Текст')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    objects = models.Manager()

    class Meta:
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created'])
        ]

    def __str__(self):
        return f'{self.food}, {self.author}, {self.date_created}'


class Like(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='likes', verbose_name='Рецепт')
    user = models.ForeignKey(User, default=User, on_delete=models.CASCADE, related_name='likes', verbose_name='Юзер')
    like = models.BooleanField(default=True, verbose_name='Лайк')

    objects = models.Manager()

    class Meta:
        ordering = ['food']
        indexes = [
            models.Index(fields=['food']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f'{self.food}, {self.user}'


class StepFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='steps', verbose_name='Рецепт')
    image = models.ImageField(upload_to=f'food/food_steps/%Y/%d', null=True, blank=True, verbose_name='Картинка')
    text = models.TextField(max_length=1000, verbose_name='Текст')

    objects = models.Manager()

    def __str__(self):
        return f'{self.food}, {self.text}'
