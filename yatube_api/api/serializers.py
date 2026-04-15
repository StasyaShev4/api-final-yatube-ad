"""Сериализаторы API приложения."""

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Follow
from django.contrib.auth import get_user_model
from posts.models import Comment, Post, Group


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Настройки сериализатора Post."""

        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Настройки сериализатора Comment."""

        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Настройки сериализатора Group."""

        model = Group
        fields = '__all__'


User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        """Настройки сериализатора Follow."""

        model = Follow
        fields = ['user', 'following']

    def validate_following(self, value):
        """Проверяет, что пользователь не подписывается на себя."""
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return value

    def validate(self, data):
        """Проверяет уникальность подписки."""
        user = self.context['request'].user
        following = data.get('following')

        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                'Подписка уже существует'
            )
        return data
