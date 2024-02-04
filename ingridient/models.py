from django.db import models
from dish.models import Dish
# Create your models here.

class IngridientItem(models.Model):
    ingridients = models.ForeignKey('Ingridient',on_delete = models.CASCADE,related_name = 'items')
    dish = models.ForeignKey(Dish,on_delete = models.CASCADE,related_name ='items')
    quantity = models.PositiveIntegerField()


class Ingridient(models.Model):
    CATEGORY_CHOICES = (
        ('Fruit','Фрукты'),
        ('Vegetable','Овощи'),
        ('Grocery','Бакалея'),
        ('Dairy','Молочные продукты'),
        ('Meet','Мясные изделия'),
        ('Sweet','Сладости'),
    )
    dishes = models.ManyToManyField(Dish,through=IngridientItem,related_name='ingridients')
    name = models.CharField(max_length = 100,unique = True)
    category = models.CharField(choices = CATEGORY_CHOICES,max_length = 100)
    

