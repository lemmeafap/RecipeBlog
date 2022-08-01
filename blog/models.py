from django.db import models
from django.urls import reverse  # Строит ссылку по имени
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название категории')
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'pk': self.pk})

    def __repr__(self):
        return f'Категория: (pk={self.pk}, title={self.title})'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Recipe(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название рецепта')
    content = models.TextField(blank=True, verbose_name='Описание')
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Имя пользователя')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    watches = models.IntegerField(default=0, verbose_name='Просмотры')
    slug = models.SlugField(unique=True, null=True)
    time_to_cook = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Статья: (pk={self.pk}, title={self.title})'

    def get_photo(self):
        if self.photo:
            return self.photo.url

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='Комментарии')
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Имя пользователя')
    content = models.TextField(verbose_name='Комментарий')
    created_on = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.content


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'
