from rest_framework import serializers
from infra.models import BarberUser
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class BarberUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = BarberUser
        fields = ('user', 'phone_number')
