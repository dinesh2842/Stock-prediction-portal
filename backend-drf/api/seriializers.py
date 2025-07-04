from rest_framework import serializers

class StockzSerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=20)
    