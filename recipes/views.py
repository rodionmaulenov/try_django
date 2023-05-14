from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse

from recipes.forms import RecipeForm, RecipeIngredientForm, ImageUploadForm
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
def recipe_delete(request, id=None):
    try:
        object = Recipe.objects.get(id=id, user=request.user)
    except:
        object = None

    if object is None:
        if request.htmx:
            return HttpResponse('NotFound')
        raise Http404()

    if request.method == 'POST':
        object.delete()
        success_url = reverse('recipes:list')
        if request.htmx:
            header = {
                'HX-Redirect': success_url
            }
            return HttpResponse('Success', headers=header)
        return redirect(success_url)
    context = {
        "object": object
    }
    return render(request, "recipes/delete.html", context)


@login_required
def recipe_ingredient_delete(request, parent_id=None, id=None):
    try:
        object = RecipeIngredient.objects.get(id=id, recipe__id=parent_id)
    except:
        object = None

    if object is None:
        if request.htmx:
            return HttpResponse('NotFound')
        raise Http404()

    obj_htmx = object

    if request.method == 'POST':
        object.delete()
        success_url = reverse('recipes:update', kwargs={'id': parent_id})
        if request.htmx:
            return render(request, "recipes/partials/ingredient-inline-remove.html", {'object': obj_htmx})
        return redirect(success_url)
    context = {
        "object": object
    }
    return render(request, "recipes/delete.html", context)


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
    new_ingredient_url = reverse('recipes:hx-ingredient-create', kwargs={'parent_id': obj.id})
    context = {
        "form": form,
        "object": obj,
        "new_ingredient_url": new_ingredient_url
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


@login_required
def image_upload_view(request, parent_id=None):
    try:
        parent_instance = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_instance = None
    if parent_instance is None:
        raise Http404()

    form = ImageUploadForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        recipe_image = form.save(commit=False)
        recipe_image.recipe = parent_instance
        recipe_image.save()
    context = {'form': form}
    return render(request, 'recipes/image-upload-form.html', context)