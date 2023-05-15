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
from django.urls import include, path

from search.views import search_view
from trydjango.views import home_page
from accounts.views import login_view, logout_view, register_user
from meals.views import meal_toggle_queue_view

urlpatterns = [
    # custom
    path('', home_page, name='home_page'),
    path('search/', search_view, name='search'),
    path('library/recipes/', include('recipes.urls')),
    path('article/', include('articles.urls')),
    path('meal-toggle/<int:recipe_id>/', meal_toggle_queue_view, name='meal-toggle'),
    # admin
    path('admin/', admin.site.urls),
    # register
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_user, name='register'),
]
