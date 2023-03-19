from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

import requests
import status

from .models import Cryptocurrency
from .serializers import CryptocurrencySerializer
from .forms import NewUserForm


def get_cryptocurrency_object(symbol):

    url_name = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?symbol={symbol}'
    url_price = f'https://api.kucoin.com/api/v1/market/stats?symbol={symbol}-USDT'

    headers = {
        'Accepts': 'application/json',
        f'X-CMC_PRO_API_KEY': settings.COINAPI_KEY,
    }

    response = requests.get(url_name, headers=headers)
    if response.status_code == 200:
        name = response.json()['data'][symbol][0]['name']
    else:
        return Response('Cryptocurrency not found', status=status.HTTP_400_BAD_REQUEST)

    response = requests.get(url_price)
    if response.status_code == 200:
        price = response.json()['data']['buy']
        market_volume = response.json()['data']['vol']
        change = response.json()['data']['changePrice']
    else:
        return Response('Cryptocurrency not found', status=status.HTTP_400_BAD_REQUEST)

    cryptocurrency = Cryptocurrency(
        symbol=symbol,
        name=name,
        price=price,
        market_volume=market_volume,
        change=change
    )

    return cryptocurrency


class AddCryptocurrency(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        if 'symbol' not in request.data:
            return Response('The request body must have a parameter [symbol]', status=status.HTTP_400_BAD_REQUEST)

        symbol = request.data['symbol'].upper()

        if Cryptocurrency.objects.filter(symbol=symbol).exists():
            return Response('This cryptocurrency is already in the database', status=status.HTTP_400_BAD_REQUEST)

        cryptocurrency = get_cryptocurrency_object(symbol)
        cryptocurrency.save()

        serializer = CryptocurrencySerializer(cryptocurrency)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCryptocurrency(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        if 'symbol' not in request.data:
            return Response('The request body must have a parameter [symbol]', status=status.HTTP_400_BAD_REQUEST)

        symbol = request.data['symbol'].upper()

        if not Cryptocurrency.objects.filter(symbol=symbol).exists():
            return Response('Cryptocurrency is not in the database', status=status.HTTP_400_BAD_REQUEST)

        cryptocurrency_id = Cryptocurrency.objects.get(symbol=symbol).id
        cryptocurrency = get_cryptocurrency_object(symbol)
        cryptocurrency.id = cryptocurrency_id
        cryptocurrency.save()

        serializer = CryptocurrencySerializer(cryptocurrency)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        if 'symbol' not in request.data:
            return Response('The request body must have a parameter [symbol]', status=status.HTTP_400_BAD_REQUEST)

        symbol = request.data['symbol'].upper()

        if not Cryptocurrency.objects.filter(symbol=symbol).exists():
            return Response('Cryptocurrency is not in the database', status=status.HTTP_400_BAD_REQUEST)

        cryptocurrency = Cryptocurrency.objects.get(symbol=symbol)
        cryptocurrency.delete()

        return Response(status=status.HTTP_200_OK)


class AllCryptocurrencyView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        queryset = Cryptocurrency.objects.all()
        print(queryset)
        serializer = CryptocurrencySerializer(queryset, many=True)
        return Response(serializer.data)


class SpecificCryptocurrencyView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, symbol):
        if Cryptocurrency.objects.filter(symbol=symbol.upper()).exists():
            return Cryptocurrency.objects.get(symbol=symbol.upper())
        return Response('Cryptocurrency not found', status=status.HTTP_404_NOT_FOUND)

    def get(self, request, symbol):

        if not Cryptocurrency.objects.filter(symbol=symbol.upper()).exists():
            return Response('Cryptocurrency is not in the database', status=status.HTTP_400_BAD_REQUEST)

        cryptocurrency = Cryptocurrency.objects.get(symbol=symbol)
        serializer = CryptocurrencySerializer(cryptocurrency)
        return Response(serializer.data)


def register_request(request):

    if request.user.id is not None:
        return redirect('index')
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('index')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):

    if request.user.id is not None:
        return redirect('index')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):

    logout(request)
    messages.info(request, "You have successfully logged out.")

    return redirect('index')


def index(request):

    cryptocurrency_list = Cryptocurrency.objects.all()
    template = 'index.html'

    return render(request, template, context={"cryptocurrency_list": cryptocurrency_list})


def search(request):

    search_text = request.GET.get('s').upper()
    cryptocurrency_list = Cryptocurrency.objects.filter(symbol=search_text)
    template = 'index.html'

    return render(request, template, context={"cryptocurrency_list": cryptocurrency_list})


def favourites(request):

    if request.user.id is None:
        return redirect('login')
    user = request.user
    template = 'favourites.html'
    try:
        cryptocurrency_list = Cryptocurrency.objects.filter(favourites=user)
    except Exception:
        return render(request, template)

    return render(request, template, context={"cryptocurrency_list": cryptocurrency_list})


def add_to_favourites(request):

    if request.user.id is None:
        return redirect('login')
    symbol = request.GET.get('symbol')
    user = request.user
    cryptocurrency = Cryptocurrency.objects.get(symbol=symbol)
    cryptocurrency.favourites.add(user)

    return redirect('favourites')


def add_to_favourites(request):

    if request.user.id is None:
        return redirect('login')
    symbol = request.GET.get('symbol')
    user = request.user
    cryptocurrency = Cryptocurrency.objects.get(symbol=symbol)
    cryptocurrency.favourites.add(user)

    return redirect('favourites')


def delete_from_favourites(request):

    if request.user.id is None:
        return redirect('login')
    symbol = request.GET.get('symbol')
    user = request.user
    cryptocurrency = Cryptocurrency.objects.get(symbol=symbol)
    cryptocurrency.favourites.remove(user)

    return redirect('favourites')


def news(request):

    articles = []
    url_news = 'https://newsapi.org/v2/everything?q=cryptocurrency&from=2023-02-18&sortBy=publishedAt&apiKey=1cd0718fc85049a29dafce6e2d07d792'
    response = requests.get(url_news)
    data = response.json()
    for i in data['articles']:
        article = [i['title'], i['description'], i['url'], i['publishedAt']]
        articles.append(article)
    print(articles[1][1])
    template = 'news.html'

    return render(request, template, context={"articles": articles})

