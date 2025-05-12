import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import Account
from invoice.models import Invoice, InvoiceItem
from django.db.models import F


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ('invoice_id', 'quantity', 'product_id', 'price')
        read_only_fields = ('invoice_id',)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('account', 'order_id', 'items')

    items = InvoiceItemSerializer(many=True)

    def create(self, validated_data):
        items = validated_data.pop('items')
        logging.warning(validated_data)
        logging.warning('Creating invoice')
        invoice = Invoice.objects.create(**validated_data)
        for item in items:
            InvoiceItem.objects.create(invoice=invoice, **item)
        Account.objects.filter(pk=invoice.account.id).update(balance=F('balance') - invoice.total_price)
        return invoice

    def validate(self, attrs):
        items = attrs.get('items', [])
        total_price = sum([item.get('price') * item.get('quantity') for item in items])
        # account = Account.objects.get(pk=attrs.get('account'))
        account = attrs.get('account')
        if account.balance < total_price:
            logging.warning('Not enough money on account')
            raise ValidationError('Not enough money on account')
        return attrs
