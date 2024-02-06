from django.db import models
from django.contrib.auth import get_user_model
from dish.models import Dish

User = get_user_model()

class Rating(models.Model):
    RATING_CHOICES = (
        (1,'Too bad'),
        (2,'Bad'),
        (3,'Normal'),
        (4,'Good'),
        (5,'Perfect')
    )
    dish = models.ForeignKey(Dish,on_delete = models.CASCADE,related_name = 'rating')
    owner = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'ratings')
    rating = models.PositiveSmallIntegerField(choices = RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)