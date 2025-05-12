import os
import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from order.settings import DEBUG
from orders.models import Order, Cart, CartItem
from orders.serializers import OrderSerializer, CartSerializer, AddItemSerializer
from logging import getLogger
l = getLogger(__name__)

GET_USER_ID_URL = 'http://{}/api/users/{}/'.format(os.environ.get('ACCOUNTS_ROOT_URL'), '{}')
FINANCIAL_PAY_URL = 'http://{}/api/accounts/{}/pay/'.format(os.environ.get('FINANCIAL_ROOT_URL'), '{}')
GET_PRICE_URL = 'http://{}/api/products/{}/'.format(os.environ.get('PRODUCTS_ROOT_URL'), '{}')


def get_user_id(username):
    kwargs = {}
    if DEBUG:
        headers = {'Host': '0.0.0.0'}
        kwargs['headers'] = headers
    resp = requests.get(GET_USER_ID_URL.format(username), **kwargs).json()
    l.warning(resp)
    print(resp)
    return resp['id']


class OrderViewSet(ReadOnlyModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = get_user_id(self.kwargs.get('username'))
        return Order.objects.filter(user_id=user_id)

    @action(detail=False, methods=['post']) #, url_path=r'(?P<username>[^/.]+)/checkout')
    def checkout(self, request, username=None):
        user_id = get_user_id(username)
        cart = Cart.objects.filter(user_id=user_id, status='active').first()
        if not cart:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        total = 0
        for item in cart.cartitem_set.all():
            total += item.price * item.quantity
        order = Order.objects.create(
            user_id=user_id,
            status='completed',
            total=total,
        )
        kwargs = {'headers': {'Host': '0.0.0.0'}} if DEBUG else {}
        pay_response = requests.post(
            FINANCIAL_PAY_URL.format(username),
            json={
                'order_id': order.id,
                'user_id': user_id,
                'items': [
                    {
                        'product_id': item.product_id,
                        'quantity': item.quantity,
                        'price': item.price,
                    }
                    for item in cart.cartitem_set.all()
                ]
            },
            **kwargs,
        )
        l.warning(pay_response.json())
        l.warning(pay_response.request.body)
        if not pay_response.ok:
            l.warning('pay_response is not ok')
            order.status = 'canceled'
            order.save()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cart.status = 'ordered'
        cart.order = order
        cart.save()
        return Response(status=status.HTTP_200_OK)


class CartViewSet(ReadOnlyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        user_id = get_user_id(self.kwargs.get('username'))
        return Cart.objects.filter(user_id=user_id)

    @swagger_auto_schema(request_body=AddItemSerializer, responses={200: CartSerializer}, method='post')
    @action(detail=False, methods=['post']) #, url_path=r'(?P<username>[^/.]+)/add-to-cart')
    def add_to_cart(self, request, username=None):
        serializer = AddItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        user_id = get_user_id(username)
        # user_id = requests.get('xxx'.format(pk), **kwargs).json()['id']
        cart = Cart.objects.filter(user_id=user_id, status='active').first()
        if not cart:
            cart = Cart.objects.create(user_id=user_id, status='active')
        kwargs = {'headers': {'Host': '0.0.0.0'}} if DEBUG else {}
        price = requests.get(GET_PRICE_URL.format(data['product_id']), **kwargs).json()['price']
        CartItem.objects.create(
            cart=cart,
            product_id=data['product_id'],
            quantity=data['quantity'],
            price=price,
        )
        return Response(status=status.HTTP_200_OK)
