from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

    # def validate_password(self, password):
    #     return password


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserCreateSerializer(UserBaseSerializer):
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError('User already exists!')
