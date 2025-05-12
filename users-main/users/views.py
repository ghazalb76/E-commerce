import os

import requests
from rest_framework.viewsets import ModelViewSet
from dotenv import load_dotenv

from users.models import User
from users.serializers import UserSerializer

load_dotenv()

CREATE_ACCOUNT_URL = 'http://{}/api/accounts/'.format(os.environ.get('FINANCIAL_ROOT_URL'))


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def perform_create(self, serializer):
        super().perform_create(serializer)
        account_data = requests.post(
            CREATE_ACCOUNT_URL,
            json={
                'user_id': serializer.data.get('id')
            },
            headers={
                'Host': '0.0.0.0',
            }
        ).json()
