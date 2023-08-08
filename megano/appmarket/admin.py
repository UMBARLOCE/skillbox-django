from django.contrib import admin
from . import models


@admin.register(models.CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "parent"]
    list_display_links = ["pk", "title"]
    ordering = ["pk"]


@admin.register(models.ImageCatalogItem)
class ImageCatalogItemAdmin(admin.ModelAdmin):
    list_display = ["pk", "catalog_item", "image", "src", "alt"]
    ordering = ["pk"]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "category"]
    list_display_links = ["pk", "title"]
    ordering = ["pk"]


@admin.register(models.ImageProduct)
class ImageProductAdmin(admin.ModelAdmin):
    list_display = ["pk", "product", "image", "src", "alt"]
    ordering = ["pk"]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["pk", "author", "product", "rate"]
    ordering = ["pk"]


@admin.register(models.Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "value"]
    ordering = ["pk"]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    ordering = ["pk"]


@admin.register(models.Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]
    list_display_links = ["pk"]
    ordering = ["pk"]
