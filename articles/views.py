from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from articles.forms import ArticleCreateNewForm
from articles.models import Article


@login_required
def article_create(request):
    form = ArticleCreateNewForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        form.save()
        context['form'] = ArticleCreateNewForm()
        # context['object'] = obj
        # context['created'] = True
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
