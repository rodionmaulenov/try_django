from django.shortcuts import render

from recipes.models import Recipe
from articles.models import Article

REQUEST_SEARCH_TYPE = {
    'article': Article,
    'recipe': Recipe
}


def search_view(request):
    query = request.GET.get('query')
    search_type = request.GET.get('type')

    Klass = Recipe

    if search_type in REQUEST_SEARCH_TYPE.keys():
        Klass = REQUEST_SEARCH_TYPE[search_type]

    queryset = Klass.objects.search(query=query)

    context = {
        'queryset': queryset
    }

    template = 'search/partials/result-view.html'
    if request.htmx:
        context = {
            'queryset': queryset[:2]
        }
        template = 'search/partials/result.html'
    return render(request, template, context)
