from django.db import models
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
    image = models.ImageField(upload_to='media')
    

