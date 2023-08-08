from django.urls import path
from . import views


app_name = "appusers"

urlpatterns = [
    path("api/profile/password", views.PasswordAPIView.as_view(), name="password"),
    path("api/profile/avatar", views.AvatarAPIView.as_view(), name="avatar"),
    path("api/profile", views.ProfileAPIView.as_view(), name="profile"),
    path("api/sign-out", views.SignOut.as_view(), name="sign-out"),
    path("api/sign-in", views.SignIn.as_view(), name="sign-in"),
    path("api/sign-up", views.SignUp.as_view(), name="sign-up"),
]
