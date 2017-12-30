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
        fields = ('username', 'password', 'first_name', 'last_name', 'email',
                'profile',)
        extra_kwargs = {'email': {'required': 'True'}}
        write_only_fields = ('password',)

    def to_representation(self, obj):
        ret = super(UserSerializer, self).to_representation(obj)
        ret.pop('password')
        return ret

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        profile = data.pop('profile')
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

        data[ 'profile' ] = profile
        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        # updates the phone_number in the profile of the user
        profile_dict = validated_data.get('profile', None)
        if profile_dict:
            phone_number = profile_dict['phone_number']
            profile = Profile.objects.get(user=instance)
            profile.phone_number = phone_number
            profile.save()
        instance.save()
        return instance
