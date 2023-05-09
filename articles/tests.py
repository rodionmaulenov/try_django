from django.test import TestCase
from django.utils.text import slugify
from django.db.utils import IntegrityError

from articles.models import Article
from articles.utils import slugify_instance_title


# Create your tests here.
class SlugTest(TestCase):
    def setUp(self) -> None:
        self.number_instances = 5
        for x in range(0, self.number_instances):
            Article.objects.create(title='Hello World', content='Some text')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_instances)

    def test_first_obj_slug_in_database(self):
        obj = Article.objects.all().order_by('id').first()
        obj_title = obj.title
        obj_slug = obj.slug
        slugify_title = slugify(obj_title)
        self.assertEqual(obj_slug, slugify_title)

    def test_obj_slug_in_database_not_equal(self):
        qs = Article.objects.exclude(slug__iexact='hello-world')
        for obj in qs:
            obj_title = obj.title
            obj_slug = obj.slug
            slugify_title = slugify(obj_title)
            self.assertNotEquals(obj_slug, slugify_title)

    def test_custom_slugify(self):
        obj = Article.objects.all().last()
        slug_list = []
        for x in range(0, 5):
            slugify_title = slugify_instance_title(obj, save=False)
            slug_list.append(slugify_title.slug)
        unique_list = list(set(slug_list))
        self.assertEqual(len(slug_list), len(unique_list))

    def test_custom_slugify_value_list(self):
        slug_list = Article.objects.values_list('slug', flat=True)
        unique_list = list(set(slug_list))
        self.assertEqual(len(slug_list), len(unique_list))

    def test_slug_unique(self):
        user_slug = Article.objects.all().first().slug
        with self.assertRaises(IntegrityError, msg='Not UNIQUE constraint failed'):
            Article.objects.create(slug=user_slug, title='Hellow world2', content='Some text2')

    def test_article_manager(self):
        qs = Article.objects.search(query='Hello World')
        self.assertEqual(qs.count(), 5)
        qs = Article.objects.search(query='World')
        self.assertEqual(qs.count(), 5)
        qs = Article.objects.search(query='Some text')
        self.assertEqual(qs.count(), 5)
