from django.contrib.auth import get_user_model
from django.db import models

from dish.models import Dish


User = get_user_model()

class Like(models.Model):
    dish = models.ForeignKey(
        Dish,
        related_name='likes',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=models.CASCADE
    )

class Favorite(models.Model):
   dish = models.ForeignKey(
        Dish,
        related_name='favorites',
        on_delete=models.CASCADE
    )
   owner = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE
    )
