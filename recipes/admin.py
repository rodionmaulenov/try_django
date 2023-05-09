from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from recipes.models import Recipe, RecipeIngredient


class RecipeIngredientInlines(admin.StackedInline):
    model = RecipeIngredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInlines]
    list_display = ['user', 'name', 'description', 'timestamp', 'created', 'active']
    readonly_fields = ['timestamp', 'created', 'active']
    raw_id_fields = ['user']


admin.site.register(Recipe, RecipeAdmin)
