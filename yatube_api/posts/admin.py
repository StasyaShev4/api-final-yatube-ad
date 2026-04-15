"""Регистрация моделей в админке."""

from django.contrib import admin
from .models import Post, Comment, Group

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Group)
