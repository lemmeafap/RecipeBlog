from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Category, Recipe, Comment, FavoriteRecipe
from .forms import RecipeForm, RegistrationForm, LoginForm, CommentForm
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib import messages
from django.views.generic.base import View


class RecipeList(ListView):
    model = Recipe
    template_name = 'blog/index.html'
    context_object_name = 'recipes'
    extra_context = {
        'title': 'Главное меню'
    }

    def get_queryset(self):
        return Recipe.objects.filter(is_published=True)


class RecipeByCategory(RecipeList):
    def get_queryset(self):
        return Recipe.objects.filter(
            category_id=self.kwargs['pk'], is_published=True
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'"{category.title}"'
        return context


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'blog/recipe_detail.html'

    def get_queryset(self):
        return Recipe.objects.filter(pk=self.kwargs['pk'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        recipe.watches += 1
        recipe.save()
        context['title'] = f'Рецепт: {recipe.title}'

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(recipe_id=self.kwargs['pk'])

        return context


class NewRecipe(CreateView):
    model = Recipe
    template_name = 'blog/recipe_form.html'
    form_class = RecipeForm
    extra_context = {
        'title': '🍽Рецепт'
    }


class RecipeUpdate(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'blog/recipe_form.html'


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('index')
    context_object_name = 'recipe'


class SearchResult(RecipeList):
    def get_queryset(self):
        word = self.request.GET.get('q')
        recipes = Recipe.objects.filter(
            Q(title__contains=word) | Q(content__icontains=word), is_published=True
        )
        return recipes

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы успешно авторизовались!')
                return redirect('index')
            else:
                messages.error(request, 'Неверные данные, проверьте еще раз!')
                return redirect('login')
        else:
            messages.error(request, 'Неверные данные, проверьте еще раз!')
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }
    return render(request, 'blog/user_login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, message='Вы успешно вышли из аккаунта')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Аккаунт успешно создан! Авторизуйтесь.')
            return redirect('login')
    else:
        form = RegistrationForm()
        context = {
            'form': form,
            'title': 'Имя пользователя'
        }

    return render(request, 'blog/register.html', context)


def save_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = request.user
            comment.recipe = Recipe.objects.get(pk=pk)
            comment.save()
        return redirect('recipe_detail', pk)


def profile(request):
    return render(request, 'blog/profile.html')


def save_or_delete_favorite_recipes(request, pk):
    user = request.user if request.user.is_authenticated else None
    recipe = Recipe.objects.get(pk=pk)
    if user:
        favorite_recipes = FavoriteRecipe.objects.filter(user=user)
        if recipe in [i.recipe for i in favorite_recipes]:
            fav_recipe = FavoriteRecipe.objects.get(user=user, recipe=recipe)
            fav_recipe.delete()
        else:
            FavoriteRecipe.objects.create(user=user, recipe=recipe)

    next_page = request.META.get('HTTP_REFERER', 'index')
    return redirect(next_page)


class FavoriteRecipesView(ListView):
    model = FavoriteRecipe
    context_object_name = 'recipes'
    template_name = 'blog/favorite_recipes.html'

    def get_queryset(self):
        user = self.request.user
        fav = FavoriteRecipe.objects.filter(user=user)
        recipes = [i.recipe for i in fav]
        return recipes
