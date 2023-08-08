import datetime
from rest_framework import serializers
from . import models


class ImageCatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageCatalogItem
        fields = ["src", "alt"]


class SubcategoriesSerializer(serializers.ModelSerializer):
    image = ImageCatalogItemSerializer(required=False)

    class Meta:
        model = models.CatalogItem
        fields = ["id", "title", "image", "subcategories"]


class CatalogItemSerializer(serializers.ModelSerializer):
    image = ImageCatalogItemSerializer(required=False)
    subcategories = SubcategoriesSerializer(many=True, required=False)

    class Meta:
        model = models.CatalogItem
        fields = ["id", "title", "image", "subcategories"]


class ImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageProduct
        fields = ["src", "alt"]


class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = models.Review
        fields = ["author", "email", "text", "rate", "date"]

    def get_date(self, instance):
        date = instance.date + datetime.timedelta(hours=2)
        return datetime.datetime.strftime(date, "%d.%m.%Y %H:%M")


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specification
        fields = ["id", "name", "value"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    images = ImageProductSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Product
        fields = "__all__"


class SaleSerializer(serializers.ModelSerializer):
    images = ImageProductSerializer(many=True)
    dateFrom = serializers.DateField(format="%d-%m")
    dateTo = serializers.DateField(format="%d-%m")

    class Meta:
        model = models.Sale
        fields = "__all__"


class ProductShortSerializer(serializers.ModelSerializer):
    images = ImageProductSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    specifications = SpecificationSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Product
        fields = "__all__"

    def get_reviews(self, obj):
        return obj.reviews.count()
