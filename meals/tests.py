from django.test import TestCase
from django.contrib.auth.models import User

from recipes.models import Recipe, RecipeIngredient
from meals.models import Meal, MealChoices


class MealTestCase(TestCase):
    def setUp(self) -> None:
        self.user_a = User.objects.create_user('rodion', password='abc123')
        self.user_id = self.user_a.id

        self.recipe_a = Recipe.objects.create(
            user=self.user_a,
            name='Chicken Grill'
        )
        self.recipe_b = Recipe.objects.create(
            user=self.user_a,
            name='Chicken Grill2'
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

        self.meal = Meal.objects.create(
            user=self.user_a,
            recipe=self.recipe_a
        )

        self.meal_b = Meal.objects.create(
            user=self.user_a,
            recipe=self.recipe_a,
            status=MealChoices.ABORTED
        )

    def test_meal_user(self):
        meal = Meal.objects.filter(user=self.user_a)
        self.assertEqual(meal.count(), 2)

    def test_meal_user_pending(self):
        meal = Meal.objects.filter(user=self.user_a, status=MealChoices.PENDING)
        self.assertEqual(meal.count(), 1)

    def test_meal_user_aborted(self):
        meal = Meal.objects.filter(user=self.user_a, status=MealChoices.ABORTED)
        self.assertEqual(meal.count(), 1)

    def test_meal_toggle_in_queue_exists(self):
        meal_b = Meal.objects.create(
            user=self.user_a,
            recipe=self.recipe_a
        )
        qs1 = Meal.objects.all().by_user_id(self.user_a).pending()
        self.assertEqual(qs1.count(), 2)
        added = Meal.objects.toggle_in_queue(self.user_id, self.recipe_a.id)
        qs2 = Meal.objects.all().by_user_id(self.user_a).aborted()
        self.assertEqual(qs2.count(), 3)
        self.assertFalse(added)

    def test_meal_toggle_in_queue_not_exists(self):

        qs1 = Meal.objects.all().by_user_id(self.user_a).pending()
        self.assertEqual(qs1.count(), 1)
        added = Meal.objects.toggle_in_queue(self.user_id, self.recipe_b.id)
        qs2 = Meal.objects.all().by_user_id(self.user_a).pending()
        self.assertEqual(qs2.count(), 2)
        self.assertTrue(added)
