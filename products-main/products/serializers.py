from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        lookup_field = 'name'
        model = Product
        fields = ('id', 'name', 'quantity', 'price')
