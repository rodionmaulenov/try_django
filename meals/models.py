from django.db import models
from django.conf import settings

from recipes.models import Recipe


class MealQuerySet(models.QuerySet):
    def by_user_id(self, user_id):
        return self.filter(user_id=user_id)

    def user(self, user):
        return self.filter(user=user)

    def pending(self):
        return self.filter(status=MealChoices.PENDING)

    def expired(self):
        return self.filter(status=MealChoices.EXPIRED)

    def aborted(self):
        return self.filter(status=MealChoices.ABORTED)

    def completed(self):
        return self.filter(status=MealChoices.COMPLETED)

    def in_queue(self, recipe_id):
        return self.pending().filter(recipe_id=recipe_id).exists()


class MealManager(models.Manager):
    def get_queryset(self):
        return MealQuerySet(self.model, self._db)

    def toggle_in_queue(self, user_id, recipe_id):
        qs = self.get_queryset().all().by_user_id(user_id)
        already_queued = qs.in_queue(recipe_id)
        added = None
        if already_queued:
            recipe_qs = qs.filter(recipe_id=recipe_id)
            recipe_qs.update(status=MealChoices.ABORTED)
            added = False
        else:
            meal = Meal(
                user_id=user_id,
                recipe_id=recipe_id,
                status=MealChoices.PENDING
            )
            meal.save()
            added = True
        return added


class MealChoices(models.TextChoices):
    PENDING = ('p', 'Pending')
    EXPIRED = ('e', 'Expired')
    ABORTED = ('a', 'Aborted')
    COMPLETED = ('c', 'Completed')


class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=MealChoices.choices, default=MealChoices.PENDING)

    objects = MealManager()
