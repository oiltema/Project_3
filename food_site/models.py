from django.db import models
from PIL import Image

from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class Food(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=20, verbose_name='Слаг')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food', verbose_name='Автор')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    time_cook = models.PositiveIntegerField(default=0, verbose_name='Время готовки')
    portion = models.PositiveIntegerField(default=1, verbose_name='Порций')
    products = models.TextField(max_length=2000, verbose_name='Продукты')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(upload_to=f'food/{title}', blank=True, null=True, verbose_name='Изображение')

    objects = models.Manager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created'])
        ]

    def __str__(self):
        return f'{self.title}, {self.author}, {self.date_created}'

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


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

