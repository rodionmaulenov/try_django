from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse

from meals.models import Meal
from recipes.models import Recipe


def meal_toggle_queue_view(request, recipe_id=None):
    if not request.htmx:
        return HttpResponseBadRequest()
    user = request.user
    if not user.is_authenticated:
        return HttpResponse('Must be logged in', status=400)
    user_id = user.id
    if request.method == 'POST':
        is_valid_recipe = False
        try:
            recipe = Recipe.objects.get(user=user, id=recipe_id)
            is_valid_recipe = True
        except:
            pass
        if is_valid_recipe:
            Meal.objects.toggle_in_queue(user_id, recipe_id)
    is_pending = Meal.objects.all().by_user_id(user_id).in_queue(recipe_id)
    togged_label = 'Add to meals' if not is_pending else 'Remove from meals'
    context = {
        'recipe_id': recipe_id,
        'in_pending': is_pending,
        'togged_label': togged_label,
    }
    return render(request, 'meals/partials/meal-toggle-queue.html', context)
