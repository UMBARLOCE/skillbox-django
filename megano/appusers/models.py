from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.user.username}_profile"


def profile_avatar_directory_path(instance: "Avatar", filename: str) -> str:
    return "profiles/profile_{pk}/avatar/{filename}".format(
        pk=instance.profile.user_id,
        filename=filename,
    )


class Avatar(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="avatar"
    )
    avatar = models.ImageField(
        null=True, blank=True, upload_to=profile_avatar_directory_path
    )

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"
        ordering = ["pk"]

    def src(self):
        return f"{settings.MEDIA_URL}{self.avatar}"

    def alt(self):
        return f"{self.profile.user.username}_avatar"

    def __str__(self) -> str:
        return f"{self.profile.user.username}_avatar"
