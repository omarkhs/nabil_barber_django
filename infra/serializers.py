from rest_framework import serializers
from infra.models import Profile
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


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
                'profile', 'password',)


class RegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',
                'profile',)
        extra_kwargs = {'email': {'required': 'True'}}
        write_only_fields = ('password',)

    def to_representation(self, obj):
        ret = super(RegistrationSerializer, self).to_representation(obj)
        ret.pop('password')
        return ret

    # def validate_password(self, value):
        # try:
            # validators.validate_password(value)
        # except serializers.ValidationError as exc:
            # raise serializers.ValidationError(str(exc))
        # return value
    def validate(self, data):
        # validators.validate_password(password=data, user=User)
        # return data

        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        data.pop('profile')
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterUserSerializer, self).validate(data)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password( validated_data.pop('password') )
        Profile.objects.create(user=user, **profile_data)
        return user
