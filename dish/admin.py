from django.contrib import admin
from .models import Dish,IngridientItem

admin.site.register(IngridientItem)


class DishAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "ingridients":
            kwargs["queryset"] = IngridientItem.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Dish,DishAdmin)
