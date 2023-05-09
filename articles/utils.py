import random
from django.utils.text import slugify


def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        instance.slug = new_slug
    else:
        slug = slugify(instance.title)
        Klass = instance.__class__
        qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
        if qs.exists():
            random_integer = random.randint(100_000, 500_000)
            slug = f'{slug}{random_integer}'
        instance.slug = slug
        if save:
            instance.save()
    return instance
