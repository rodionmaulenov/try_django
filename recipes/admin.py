from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient, RecipeIngredientImage


class RecipeIngredientInlines(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInlines]
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'created']
    raw_id_fields = ['user']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredientImage)
