from django.contrib import admin
from recipes.models import Recipe, Ingredient, Step
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Step)
admin.site.register(Ingredient)
