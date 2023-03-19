"""crypto_view URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from rest_framework.authtoken import views

from crypto_api.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('news', news, name="search"),
    path('search', search, name="search"),
    path('add/favourites', add_to_favourites, name="add_to_favourites"),
    path('delete/favourites', delete_from_favourites, name="delete_from_favourites"),
    path('favourites', favourites, name="favourites"),
    path("logout", logout_request, name= "logout"),
    path("login", login_request, name="login"),
    path('register', register_request, name="register"),
    path('api/auth', views.obtain_auth_token, name='get_token'),
    path('api/add/cryptocurrency', AddCryptocurrency.as_view(), name='add_cryptocurrency'),
    path('api/view/сryptocurrencies', AllCryptocurrencyView.as_view(), name='сryptocurrencies_list'),
    path('api/view/сryptocurrencies/<str:symbol>', SpecificCryptocurrencyView.as_view(), name='specific_cryptocurrency'),
    path('api/update/cryptocurrency', UpdateCryptocurrency.as_view(), name='update_cryptocurrency'),
]


