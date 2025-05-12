from rest_framework import serializers

from account.models import Account
from invoice.serializers import InvoiceItemSerializer, InvoiceSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'user_id', 'balance', 'invoices')

    invoices = InvoiceSerializer(many=True, read_only=True)


class PaySerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    items = InvoiceItemSerializer(many=True)
