from django.shortcuts import render


def search_view(request):
    query = request.GET.get('q')

    context = {
        'query': query
    }
    template = 'search/partials/result-view.hml'
    if request.htmx:
        template = 'search/partials/result-view.hml'
    return render(request, template, context)