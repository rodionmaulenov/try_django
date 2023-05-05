"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from trydjango.views import home_page
from articles.views import article_search, article_create, article_detail
from accounts.views import login_view, logout_view

urlpatterns = [
    path('', home_page, name='home_page'),
    path('article/', article_search, name='home_page'),
    path('article/create/', article_create, name='home_page'),
    path('article/<int:id>/', article_detail, name='home_page'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
