from django.contrib import admin
from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "createdAt",
        "user",
        "fullName",
        "status",
        "totalCost",
        "deliveryType",
    ]
    ordering = ["pk"]
