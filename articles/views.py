from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from articles.forms import ArticleCreateNewForm
from articles.models import Article


@login_required
def article_create(request):
    form = ArticleCreateNewForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        obj = form.save()
        context['form'] = ArticleCreateNewForm()
        return redirect(obj.get_absolute_url())
    return render(request, 'articles/article_create.html', context=context)


def article_search(request):
    query = request.GET.get('query')
    objs = Article.objects.search(query)
    context = {'objs': objs}
    return render(request, 'articles/article_search.html', context=context)


def article_detail(request, slug=None):
    try:
        obj = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise ValueError('unreachable value')
    except Article.MultipleObjectsReturned:
        obj = Article.objects.filter(slug=slug).first()
    except:
        raise Http404()

    context = {'obj': obj}
    return render(request, 'articles/article_detail.html', context=context)
