from rest_framework import serializers
from infra.models import Profile
from django.contrib.auth.models import User


# Extra fields added to User class
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone_number',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                'profile',)


class RegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',
                'profile',)
        extra_kwargs = {'email': {'required': 'True'}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
