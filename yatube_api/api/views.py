"""Представления API приложения."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Follow
from .serializers import PostSerializer, CommentSerializer, GroupSerializer
from .serializers import FollowSerializer

from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """Создаёт пост с текущим пользователем как автором."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_post(self):
        """Возвращает пост по id из URL."""
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        """Возвращает список комментариев для поста."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Создаёт комментарий к посту."""
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class GroupViewSet(ReadOnlyModelViewSet):
    """Вьюсет только для чтения групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для подписок пользователей."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        """Возвращает подписки текущего пользователя."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создаёт подписку."""
        serializer.save(user=self.request.user)
