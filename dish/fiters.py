import django_filters


from dish.models import Dish
from ingridient.models import Ingridient



class DishFilter(django_filters.FilterSet):
    ingridients = django_filters.ModelMultipleChoiceFilter(field_name='ingridients', queryset=Ingridient.objects.all(),conjoined=True)

    class Meta:
        model = Dish
        fields = ['ingridients']
