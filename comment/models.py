from django.db import models
from django.contrib.auth import get_user_model


from dish.models import Dish


User = get_user_model()

class Comment(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateField(auto_now_add=True)
    dish = models.ForeignKey(
        Dish, 
        on_delete=models.CASCADE,
        related_name='comments'
    )




