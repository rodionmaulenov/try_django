from django.urls import path

from recipes.views import \
    recipe_list, recipe_create_view, recipe_detail, recipe_update_view, recipe_hx_detail, \
    recipe_hx_ingredient_update, recipe_delete, recipe_ingredient_delete, image_upload_view

app_name = 'recipes'

urlpatterns = [
    path('', recipe_list, name='list'),
    path('create/', recipe_create_view, name='create'),

    path('hx/<int:parent_id>/ingredient/<int:id>/', recipe_hx_ingredient_update,
         name='hx-ingredient-update'),
    path('hx/<int:parent_id>/ingredient/', recipe_hx_ingredient_update,
         name='hx-ingredient-create'),
    path('hx/<int:id>/', recipe_hx_detail, name='hx-detail'),

    path('<int:parent_id>/image-upload/', image_upload_view,
         name='image-upload'),
    path('delete/<int:parent_id>/ingredient/<int:id>/', recipe_ingredient_delete,
         name='ingredient-delete'),
    path('<int:id>/delete/', recipe_delete, name='delete'),
    path('<int:id>/edit/', recipe_update_view, name='update'),
    path('<int:id>/', recipe_detail, name='detail'),
]
