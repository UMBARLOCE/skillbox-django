import json
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from . import serializers


class ProfileAPIView(APIView):  # +
    """
    http://127.0.0.1:8000/api/profile 'fullName', 'email', 'phone' меняются.
    http://127.0.0.1:8000/profile/ 'fullName', 'email', 'phone' меняются.
    Но через форму при нажатии на кнопку СОХРАНИТЬ поля становятся пустыми,
    после чего можно обновить страницу и новые данные появляются в полях.
    """

    def get(self, request: Request) -> Response:
        profile = models.Profile.objects.get(user_id=request.user.pk)
        serialized = serializers.ProfileSerializer(profile, many=False)
        return Response(serialized.data)

    def post(self, request: Request) -> Response:
        data = request.data
        profile = models.Profile.objects.get(user_id=request.user.pk)
        profile.fullName = data.get("fullName")
        profile.email = data.get("email")
        profile.phone = data.get("phone")
        profile.save()
        return Response("successful operation", status=status.HTTP_200_OK)


class AvatarAPIView(GenericAPIView, UpdateModelMixin):  # +
    """
    http://127.0.0.1:8000/api/profile/avatar аватар меняется.
    http://127.0.0.1:8000/profile/ через форму аватар меняется.
    """

    serializer_class = serializers.AvatarSerializer

    def get(self, request: Request) -> Response:
        profile, created = models.Profile.objects.get_or_create(user_id=request.user.pk)
        avatar, created = models.Avatar.objects.get_or_create(profile_id=profile.pk)
        serialized = serializers.AvatarSerializer(avatar, many=False)
        return Response(serialized.data)

    def post(self, request: Request) -> Response:
        new_avatar = request.FILES["avatar"]  # request.FILES["image"]
        print(new_avatar)
        profile, created = models.Profile.objects.get_or_create(user_id=request.user.pk)
        avatar, created = models.Avatar.objects.get_or_create(profile_id=profile.pk)
        avatar.avatar = new_avatar
        avatar.save()
        return Response("successful operation", status=status.HTTP_200_OK)


class PasswordAPIView(APIView):  # +
    """
    http://127.0.0.1:8000/api/profile/password пароль меняется.
    http://127.0.0.1:8000/profile/ через форму пароль меняется.
    {
    "currentPassword": "umbarloce",
    "newPassword": "skillbox"
    }
    """

    def get(self, request: Request) -> Response:
        serialized = serializers.UserSerializer(request.user)
        return Response(serialized.data)

    def post(self, request: Request) -> Response:
        data = request.data
        user = request.user

        if user.check_password(data["currentPassword"]):
            user.set_password(data["newPassword"])
            user.save()
            return Response("successful operation", status=status.HTTP_200_OK)
        else:
            return Response(
                "unsuccessful operation", status=status.HTTP_400_BAD_REQUEST
            )


class SignOut(APIView):  # +
    """
    http://127.0.0.1:8000/api/sign-out выход из учётки.
    http://127.0.0.1:8000/ выход кнопкой из учётки.
    """

    def post(self, request: Request) -> Response:
        logout(request)
        return Response("successful operation", status=status.HTTP_200_OK)


class SignIn(APIView):  # +
    """
    http://127.0.0.1:8000/api/sign-in входит в учётку.
    http://127.0.0.1:8000/sign-in/ входит через форму в учётку.
    {
        "username": "admin",
        "password": "12345"
    }
    """

    def post(self, request: Request) -> Response:
        body = json.loads(request.body)
        username = body["username"]
        password = body["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response("successful operation", status=status.HTTP_200_OK)

        return Response(
            "unsuccessful operation", status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class SignUp(APIView):  # +
    """
    http://127.0.0.1:8000/api/sign-up создаёт учётку.
    http://127.0.0.1:8000/sign-up/ через форму создаёт учётку.
    {
        "name": "qqq",
        "username": "qqq",
        "password": "qqq"
    }
    """

    def post(self, request: Request) -> Response:
        body = json.loads(request.body)
        serialized = serializers.UserSerializer(data=body)
        if (
            serialized.is_valid()
            and not User.objects.filter(username=body.get("username")).exists()
        ):
            name = body.get("name")
            username = body.get("username")
            password = body.get("password")

            user = User.objects.create_user(
                username=username, password=password, first_name=name
            )
            profile = models.Profile.objects.create(user=user, fullName=name)

            user = authenticate(request, username=username, password=password)
            login(request, user)

            return Response("successful operation", status=status.HTTP_200_OK)
        return Response(
            "unsuccessful operation", status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
