from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from articles.models import Article


@login_required
def article_create(request):
    context = {}
    if request.method == "POST":
        obj = Article.objects.create(title=request.POST.get('title'), content=request.POST.get('content'))
        context['object'] = obj
        context['created'] = True
    return render(request, 'articles/article_create.html', context=context)


def article_search(request):
    try:
        query = int(request.GET.get('query'))
        try:
            obj = Article.objects.get(id=query)
        except Article.DoesNotExist:
            raise ValueError('unreachable value')
    except ValueError:
        raise ValueError('Must be integer')

    context = {'obj': obj}
    return render(request, 'articles/article_search.html', context=context)


def article_detail(request, id=None):
    try:
        obj = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise ValueError('unreachable value')

    context = {'obj': obj}
    return render(request, 'articles/article_detail.html', context=context)
