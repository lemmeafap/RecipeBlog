from django.urls import path
from .views import *
from .models import *

urlpatterns = [

    path('', RecipeList.as_view(), name='index'),
    path('category/<int:pk>/', RecipeByCategory.as_view(), name='category_list'),
    path('recipe/<int:pk>/', RecipeDetail.as_view(), name='recipe_detail'),
    path('add_recipe/', NewRecipe.as_view(), name='add_recipe'),
    path('recipe/<int:pk>/update/', RecipeUpdate.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', RecipeDelete.as_view(), name='recipe_delete'),
    path('search/', SearchResult.as_view(), name='search'),

    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    path('save_comment/<int:pk>', save_comment, name='save_comment'),
    path('add_or_delete_favorite/<int:pk>/', save_or_delete_favorite_recipes, name='save_or_delete'),
    path('favorite_recipes', FavoriteRecipesView.as_view(), name='favorite')

]
