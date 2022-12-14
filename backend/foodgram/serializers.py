from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import CustomUserSerializer

from .models import (Favorite, Follow, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор игредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор игредиентов в рецепте."""

    id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор вывода рецептов."""

    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True, source='ingredientinrecipe_set')
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        """Получить список избранного."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Получить список покупок."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'name', 'image', 'text', 'ingredients',
            'tags', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов."""

    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientInRecipeSerializer(
        many=True, source='ingredientinrecipe_set')
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    cooking_time = serializers.IntegerField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'name', 'image', 'text', 'ingredients',
            'tags', 'cooking_time', 'is_favorited', 'is_in_shopping_cart',)

    def validate_ingredients(self, data):
        """Валидация ингридиентов."""
        ingredients_id_list = []
        if not data:
            raise serializers.ValidationError(
                'В вашем рецепте должен быть хотя бы один ингредиент')
        for ingredient in data:
            if float(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше нуля!')
            ingredients_id_list.append(ingredient.get('id'))
        unique_ingredients = set(ingredients_id_list)
        if len(ingredients_id_list) > len(unique_ingredients):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться'
            )
        return data

    def validate_tags(self, data):
        """Валидация тэгов."""
        tag_id_list = []
        if not data:
            raise serializers.ValidationError(
                'В вашем рецепте должен быть хотя бы один тэг')
        for tag in data:
            tag_id_list.append(tag.id)
        unique_tag = set(tag_id_list)
        if len(tag_id_list) > len(unique_tag):
            raise serializers.ValidationError(
                'Тэги не должны повторяться'
            )
        return data

    def validate_cooking_time(self, data):
        """Валидация времени готовки."""
        if data <= 0:
            raise serializers.ValidationError(
                'Время приготовления блюда не может быть меньше 1 минуты')
        elif data > 500:
            raise serializers.ValidationError(
                'Время приготовления блюда не может быть больше 500 минут')
        return data

    def add_recipe_ingredient(self, ingredients, recipe):
        """Метод добавляет ингридиенты в рецепт."""
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                ingredient_id=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        """Метод создает рецепт."""
        image = validated_data.pop('image')
        tags_data = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientinrecipe_set')
        recipe = Recipe.objects.create(image=image, **validated_data)
        self.add_recipe_ingredient(ingredients, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        """Метод изменяет рецепт."""
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)
        IngredientInRecipe.objects.filter(recipe=instance).all().delete()
        ingredients = validated_data.get('ingredientinrecipe_set')
        self.add_recipe_ingredient(ingredients, instance)
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        """Получить список избранного."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Получить список покупок."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()

    def to_representation(self, instance):
        """Получить обновленный или сзданный рецепт."""
        serializer = RecipeListSerializer(instance)
        return serializer.data


class RecipeForFollowSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для получения рецепта в подписках."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, following):
        """Валидация подписки."""
        if self.context.get('request').method == 'POST':
            if self.context.get('request').user == following:
                raise serializers.ValidationError(
                    'Вы не можете стать своим подписчиком:)')
        return following

    def get_is_subscribed(self, obj):
        """Получить подписки на автора."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj.author).exists()

    def get_recipes(self, obj):
        """Получить рецепты из подписки."""
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if recipes_limit is not None:
            queryset = Recipe.objects.filter(
                author=obj.author
            )[:int(recipes_limit)]
        return RecipeForFollowSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""

    id = serializers.PrimaryKeyRelatedField(
        source='recipe.id', read_only=True
    )
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""

    id = serializers.PrimaryKeyRelatedField(
        source='recipe.id', read_only=True
    )
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')
