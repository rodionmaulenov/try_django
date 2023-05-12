from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse

from recipes.forms import RecipeForm, RecipeIngredientForm
from recipes.models import Recipe, RecipeIngredient


@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(user=request.user)
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/list.html', context)


@login_required
def recipe_detail(request, id=None):
    hx_url = reverse("recipes:hx-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "recipes/detail.html", context)


@login_required
def recipe_hx_detail(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "recipes/partials/detail.html", context)


@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.htmx:
            header = {
                'HX-Redirect': obj.get_absolute_url()
            }
            return HttpResponse('Created', headers=header)
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create_update.html", context)


@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)

    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved.'
    if request.htmx:
        return render(request, "recipes/partials/forms.html", context)
    return render(request, "recipes/create_update.html", context)


@login_required
def recipe_hx_ingredient_update(request, parent_id=None, id=None):
    if not request.htmx:
        return Http404()
    try:
        parent = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent = None
    if parent is None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(id=id, recipe=parent)
        except:
            instance = None

    form = RecipeIngredientForm(request.POST or None, instance=instance)
    url = reverse('recipes:hx-ingredient-create', kwargs={'parent_id': parent.id})
    if instance:
        url = instance.get_hx_edit_url()

    context = {
        'url': url,
        'form': form,
        "object": instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent
        new_obj.save()
        context['object'] = new_obj
        return render(request, 'recipes/partials/ingredient-inline.html', context)
    return render(request, 'recipes/partials/ingredient-form.html', context)


