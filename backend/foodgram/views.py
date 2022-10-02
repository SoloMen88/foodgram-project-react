from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .custom_mixins import RetrieveListViewSet
from .filters import IngredientsFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)
from .pagination import CustomPageNumberPaginator
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          ShoppingCartSerializer, TagSerializer)


class IngredientViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class TagViewSet(RetrieveListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = (AuthorOrReadOnly, )
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'GET':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                data = {
                    'errors': 'Рецепт уже в Избранном, загляни'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(
                favorite, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            data = {
                'errors': 'Такого рецепта нет в Избранном'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'GET':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                data = {
                    'errors': 'Этот рецепт уже есть в списке покупок'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            shopping_cart = ShoppingCart.objects.create(
                user=user, recipe=recipe)
            serializer = ShoppingCartSerializer(
                shopping_cart, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        shopping_cart = ShoppingCart.objects.filter(
            user=user, recipe=recipe
        )
        if not shopping_cart.exists():
            data = {
                'errors': 'Этого рецепта нет в списке покупок'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_list = {}
        ingredients = IngredientInRecipe.objects.filter(
            recipe__cart__user=user).values_list(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit',
                named=True)
        for ingredient in ingredients:
            name = ingredient.ingredient__name
            measurement_unit = ingredient.ingredient__measurement_unit
            amount = ingredient.amount
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount
        file_name = 'ShoppingList'
        response = HttpResponse(content_type='application/pdf')
        content_disposition = f'attachment; filename="{file_name}.pdf"'
        response['Content-Disposition'] = content_disposition
        pdfmetrics.registerFont(TTFont('Neocyr', 'Neocyr.ttf', 'UTF-8'))
        pdf = canvas.Canvas(response)
        pdf.setFont('Neocyr', 24)
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(300, 770, 'Список покупок')
        pdf.setFillColor(colors.black)
        pdf.setFont('Neocyr', 16)
        height = 700
        for name, data in shopping_list.items():
            pdf.drawString(
                60,
                height,
                f"{name} - {data['amount']} {data['measurement_unit']}"
            )
            height -= 25
            if height == 50:
                pdf.showPage()
                pdf.setFont('Neocyr', 16)
                height = 700
        pdf.showPage()
        pdf.save()
        return response
