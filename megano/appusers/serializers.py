from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Avatar
        fields = ["avatar", "src", "alt"]


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(many=False, required=False)

    class Meta:
        model = models.Profile
        fields = ["fullName", "email", "phone", "avatar"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
