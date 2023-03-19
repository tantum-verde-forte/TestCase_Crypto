from rest_framework import serializers

from .models import Cryptocurrency


class CryptocurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Cryptocurrency
        fields = ["symbol", "name", "price", "market_volume", "change"]

