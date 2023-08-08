from django.contrib import admin
from . import models


@admin.register(models.Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ["pk", "profile", "avatar", "src", "alt"]
    ordering = ["pk"]


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "fullName", "email", "phone"]
    ordering = ["pk"]
