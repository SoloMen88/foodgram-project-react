from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientInline(admin.TabularInline):
    model = IngredientInRecipe


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'text',
                    'cooking_time', 'favorited')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'

    inlines = [
        IngredientInline,
    ]

    def favorited(self, obj):
        favorited_count = Favorite.objects.filter(recipe=obj).count()
        return favorited_count

    favorited.short_description = 'В избранном'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
