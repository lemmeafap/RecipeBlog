from django.contrib import admin
from .models import Category, Recipe, Comment


# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'created_on', 'updated_on', 'is_published')
    list_display_links = ('pk', 'title')
    list_editable = ('is_published',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'recipe', 'content', 'created_on', 'publish')
    list_display_links = ('pk', 'content')
    readonly_fields = ('username', 'recipe', 'content', 'created_on')
    list_editable = ('publish', )


admin.site.register(Category)
admin.site.register(Recipe, RecipeAdmin)
