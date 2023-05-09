from django.http import HttpResponse
from django.template.loader import get_template

import random

from articles.models import Article


def home_page(request, *args, **kwargs):
    generate_id = random.randint(1, 4)
    article_obj = Article.objects.get(id=generate_id)
    articles = Article.objects.all()

    context = {
        'articles': articles,
        'article_title': article_obj.title,
        'article_content': article_obj.content,
        'article': article_obj
    }
    result = get_template('home.html').render(context)

    return HttpResponse(result)


