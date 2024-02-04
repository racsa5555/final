from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Dish(models.Model):
    CUISINE_CHOICES = (
        ('Asian','Азитаская'),
        ('Europian','Европейская'),
        ('Kyrgyz','Кыргызская'),
        ('Russian','Русская'),
        ('Japan','Японская'),
        ('Chinese','Китайская')
    )
    TYPE_CHOICES = (
        ('Snack','Закускa'),
        ('First course','Певрое блюдо'),
        ('Hot dish','Горячее блюдо'),
        ('Dessert','Десерт'),
        ('Cocktail','Коктейль'),
        ('Soup','Суп'),
        ('Salad','Салат')
    )
    name = models.CharField(max_length = 100,unique = True,null = False)
    cuisine = models.CharField(choices = CUISINE_CHOICES,max_length = 50)
    type = models.CharField(choices = TYPE_CHOICES)
    cooking_time = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='media',null = True)
    recipe = models.TextField()
    owner = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'dishes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

