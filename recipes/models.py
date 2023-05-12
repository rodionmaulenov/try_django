from django.db import models
from django.conf import settings
from django.shortcuts import reverse

import pint

from recipes.utils import number_str_to_float
from recipes.validators import check_valid_value


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'id': self.id})

    def get_edit_url(self):
        return reverse('recipes:update', kwargs={'id': self.id})

    def get_hx_url(self):
        return reverse('recipes:hx-detail', kwargs={'id': self.id})

    def get_ingredients_children(self):
        return self.recipeingredient_set.all()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[check_valid_value])
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_hx_edit_url(self):
        kwargs = {
            'id': self.id,
            'parent_id': self.recipe.id
        }
        return reverse('recipes:hx-ingredient-update', kwargs=kwargs)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def convert_to_system(self, system='mks'):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        return measurement

    def as_mks(self):
        measurement = self.convert_to_system(system='mks')
        return measurement.to_base_units()

    def as_imperial(self):
        measurement = self.convert_to_system(system='imperial')
        return measurement.to_base_units()

    def save(self, *args, **kwargs):
        quantity = self.quantity
        quantity_as_float, is_quantity_as_float = number_str_to_float(str(quantity))
        if is_quantity_as_float:
            self.quantity_as_float = quantity_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)
