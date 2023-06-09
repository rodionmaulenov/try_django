from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from recipes.models import Recipe, RecipeIngredient

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.user_a = User.objects.create_user('rodion', password='abc123')

    def test_check_user(self):
        user = self.user_a
        username = user.get_username()
        checked_password = user.check_password('abc123')
        self.assertEqual(username, user.username)
        self.assertTrue(checked_password)


class RecipesTestCase(TestCase):
    def setUp(self) -> None:
        self.user_a = User.objects.create_user('rodion', password='abc123')
        self.recipe_a = Recipe.objects.create(
            user=self.user_a,
            name='Chicken Grill'
        )
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Chicken Grill Tacco',
            quantity='1/2',
            unit='pound'
        )
        self.recipe_ingredient_b = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Chicken Grill Tacco2',
            quantity='afasfas',
            unit='kg'
        )

    def test_count_user(self):
        user = User.objects.all()
        self.assertEqual(user.count(), 1)

    def test_count_reverse_user_recipes(self):
        user = self.user_a
        recipes = user.recipe_set.all()
        self.assertEqual(recipes.count(), 1)

    def test_count_recipe_direct(self):
        user = self.user_a
        recipes = Recipe.objects.filter(user=user)
        self.assertEqual(recipes.count(), 1)

    def test_count_reverse_user_recipe_ingredient_has(self):
        user = self.user_a
        ingredient_id = user.recipe_set.values_list('recipeingredient__name', flat=True)
        recipe_ingredients = RecipeIngredient.objects.filter(name__in=ingredient_id)
        self.assertEqual(recipe_ingredients.count(), 2)

    def test_count_user_recipe_ingredient_has(self):
        user = self.user_a
        recipe_ingredients = RecipeIngredient.objects.filter(recipe__user__username=user.username)
        self.assertEqual(recipe_ingredients.count(), 2)

    def test_validate_unit_error(self):
        with self.assertRaises(ValidationError):
            invalid_unit = ['nada']
            recipe_ingredients = RecipeIngredient.objects.create(
                recipe=self.recipe_a,
                name='New',
                quantity=1.5,
                unit=invalid_unit
            )
            recipe_ingredients.full_clean()

    def test_validate_unit_without_error(self):
        valid_unit = 'kg'
        recipe_ingredients = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='New',
            quantity=1.5,
            unit=valid_unit
        )
        recipe_ingredients.full_clean()

    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)
