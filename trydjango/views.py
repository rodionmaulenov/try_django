from django.http import HttpResponse

HTML_HUMAN = "<h1>Hello World</h1>"


def home_page(request):
    return HttpResponse(HTML_HUMAN)

