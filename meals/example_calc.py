from django.contrib.auth import get_user_model
from django.db.models import Sum

from meals.models import Meal
from recipes.models import RecipeIngredient

User = get_user_model()
user = User.objects.first()

qs = Meal.objects.all().by_user_id(user.id).pending().prefetch_related('recipe__recipeingredient')
ids = qs.objects.values_list('recipe__recipeingredient__id', Flat=True)
recipe_ingredient = RecipeIngredient.objects.filter(id__in=ids)
data = recipe_ingredient.values('name', 'unit').annotate(total=Sum('quantity_as_float'))
