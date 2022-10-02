from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

foodgram_router = DefaultRouter()
foodgram_router.register(r'tags', TagViewSet, basename='tags')
foodgram_router.register(r'recipes', RecipeViewSet, basename='recipes')
foodgram_router.register(
    r'ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(foodgram_router.urls)),
]
