import os

import requests
from django.core.exceptions import ObjectDoesNotExist
from Financial.settings import DEBUG
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from dotenv import load_dotenv

from account.models import Account
from account.serializers import AccountSerializer, PaySerializer
from invoice.serializers import InvoiceSerializer

from logging import getLogger
l = getLogger(__name__)

load_dotenv()

GET_USER_ID_URL = 'http://{}/api/users/{}/'.format(os.environ.get('ACCOUNTS_ROOT_URL'), '{}')


class AccountViewset(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_value_regex = "[^/]+"

    # Get user_id from accounts service
    def get_object(self):
        l.warning(self.kwargs)
        id = self.kwargs.get('pk')
        if not id.isnumeric():
            kwargs = {'headers': {'Host': '0.0.0.0'}} if DEBUG else {}
            data = requests.get(GET_USER_ID_URL.format(id), **kwargs).json()
            return Account.objects.get(user_id=data.get('id'))
        else:
            return super().get_object()

    @swagger_auto_schema(method='post', responses={200: InvoiceSerializer}, request_body=PaySerializer)
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        serializer = PaySerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        data = serializer.validated_data
        user_id = data.pop('user_id')
        try:
            account = Account.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        invoice_serializer = InvoiceSerializer(data={'account': account.id, **data})
        if invoice_serializer.is_valid():
            invoice = invoice_serializer.save()
            return Response(data=InvoiceSerializer(instance=invoice).data)
        else:
            l.warning(invoice_serializer.errors)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
