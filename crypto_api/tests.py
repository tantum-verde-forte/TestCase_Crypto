from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from crypto_api.models import Cryptocurrency


User = get_user_model()


class CryptocurrencyAPITestCase(APITestCase):
    def setUp(self):
        User1 = User.objects.create_superuser('Test', 'TestCase@bk.ru', 'Lolipop2019')
        token = Token.objects.get_or_create(user=User1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token[0]))
        Cryptocurrency.objects.create(symbol='BTC', name='Bitcoin', price='3424', market_volume='32424', change='324234')

    def test_cryptocurrencies_view(self):

        response = self.client.get(reverse('сryptocurrencies_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_specific_cryptocurrencies_view(self):
        response = self.client.get('/api/view/сryptocurrencies/BTC')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/view/сryptocurrencies/ETH')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_cryptocurrency(self):
        response = self.client.post(reverse('update_cryptocurrency'), {'symbol': 'BTC'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(reverse('update_cryptocurrency'), {'symbol': 'btc'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse('update_cryptocurrency'), {'symbol': 'btc'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(reverse('update_cryptocurrency'), {'symbol': 'ETH'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('update_cryptocurrency'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_cryptocurrency(self):
        response = self.client.post(reverse('add_cryptocurrency'), {'symbol': 'ETH'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(reverse('add_cryptocurrency'), {'symbol': 'BTC'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('add_cryptocurrency'), {'symbol': 'doge'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(reverse('add_cryptocurrency'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
