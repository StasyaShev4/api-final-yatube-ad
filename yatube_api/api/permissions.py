"""Пользовательские permissions для API."""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешает редактирование только автору объекта."""

    def has_object_permission(self, request, view, obj):
        """Проверяет права доступа к объекту."""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
