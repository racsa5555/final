from django.db import models
from dish.models import Dish
# Create your models here.
class Ingridient(models.Model):
    CATEGORY_CHOICES = (
        ('Fruit','Фрукты'),
        ('Vegetable','Овощи'),
        ('Grocery','Бакалея'),
        ('Dairy','Молочные продукты'),
        ('Meet','Мясные изделия'),
        ('Sweet','Сладости'),
    )
    name = models.CharField(max_length = 100,unique = True)
    category = models.CharField(choices = CATEGORY_CHOICES,max_length = 100)
    

class IngridientItem(models.Model):
    ingridient = models.ForeignKey(Ingridient,on_delete = models.CASCADE,related_name = 'items')
    dish = models.ForeignKey(Dish,on_delete = models.CASCADE,related_name =models.CASCADE)
    quantity = models.PositiveIntegerField()
    