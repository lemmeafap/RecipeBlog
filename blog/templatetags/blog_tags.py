from django import template
from blog.models import Category, FavoriteRecipe

register = template.Library()


@register.simple_tag()
def get_all_categories():
    return Category.objects.all()

@register.simple_tag()
def get_favorite_recipes(user):
    fav = FavoriteRecipe.objects.filter(user=user)
    recipes = [i.recipe for i in fav]
    return recipes
