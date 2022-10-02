from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from foodgram.models import Follow
from foodgram.serializers import FollowSerializer
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=(permissions.IsAuthenticated,)
            )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        user = request.user
        check_subscribe = Follow.objects.filter(
            user=user, author=author).exists()
        if request.method == 'GET':
            if check_subscribe or user == author:
                return Response({
                    'errors': ('Вы уже подписаны на этого автора рецептов '
                               'или пытаетесь подписаться на самого себя')
                }, status=status.HTTP_400_BAD_REQUEST)
            subscribe = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                subscribe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if check_subscribe:
            Follow.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Вы не были подписаны на этого автора рецептов'
        }, status=status.HTTP_400_BAD_REQUEST)
