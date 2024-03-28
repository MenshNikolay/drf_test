from django.db import models
from django.contrib.auth.models import AbstractUser,Permission



class User(AbstractUser):
        user_permissions = models.ManyToManyField(Permission, blank=True, related_name='drf_users_permissions',)
        groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_user_set',  # Или любое другое подходящее имя
    )