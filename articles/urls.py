from django.urls import path

from articles.views import article_search, article_create, article_detail

app_name = 'articles'
urlpatterns = [
    path('', article_search, name='search'),
    path('create/', article_create, name='create'),
    path('<slug:slug>/', article_detail, name='detail'),
]
