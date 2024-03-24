from django.db import models
from django.contrib.auth.models import User
from pytils.translit import slugify
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, verbose_name='Слаг')

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save()


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory', verbose_name='Категория')
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=155, verbose_name='Слаг')

    objects = models.Manager()

    def __str__(self):
        return f'{self.category} - {self.title}'

    class Meta:
        verbose_name = 'Подкатегории'
        verbose_name_plural = 'Подкатегории'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save()


class Performer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performer', verbose_name='Пользователь')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    city = models.CharField(max_length=100, verbose_name='Город')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='performer', verbose_name='Категория')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    objects = models.Manager()

    class Meta:
        ordering = ['-date_create']
        indexes = [
            models.Index(fields=['date_create'])
        ]
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнитель'

    def __str__(self):
        return self.user.username


class TypeWork(models.Model):
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name='typework', verbose_name='Исполнитель')
    title = models.CharField(max_length=255, verbose_name='Название')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['performer']
        indexes = [
            models.Index(fields=['performer'])
        ]
        verbose_name = 'Типы работ'
        verbose_name_plural = 'Типы работ'


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.performer.id, filename)


class MyWork(models.Model):
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name='mywork', verbose_name='Исполнитель')
    image = models.ImageField(upload_to=user_directory_path, verbose_name='Изображение')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    objects = models.Manager()

    def __str__(self):
        return f'{self.performer}'

    class Meta:
        ordering = ['performer']
        indexes = [
            models.Index(fields=['performer'])
        ]
        verbose_name = 'Мои работы'
        verbose_name_plural = 'Мои работы'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review', verbose_name='Автор')
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name='review', verbose_name='Исполнитель')
    text = models.TextField(max_length=1000, verbose_name='Текст')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    objects = models.Manager()

    def __str__(self):
        return f'{self.user} - {self.date_create}'

    class Meta:
        ordering = ['performer']
        indexes = [
            models.Index(fields=['performer'])
        ]
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'
