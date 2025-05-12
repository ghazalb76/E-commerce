from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        lookup_field = 'username'
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'email')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
