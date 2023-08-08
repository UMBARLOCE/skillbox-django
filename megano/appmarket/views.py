from datetime import datetime
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from . import models
from . import serializers


class CatalogItemListAPIView(APIView):
    def get(self, request: Request):
        categories = models.CatalogItem.objects.filter(parent=None)
        serialized = serializers.CatalogItemSerializer(categories, many=True)
        return Response(serialized.data)


class ProductDetail(APIView):
    def get(self, request: Request, pk):
        product = models.Product.objects.get(pk=pk)
        serialized = serializers.ProductSerializer(product)
        return Response(serialized.data)


class ReviewCreateAPIView(CreateModelMixin, GenericAPIView):
    """
    Отзыв может оставить только зарегистрированный пользователь
    при условии заполнения в профайле emal.
    Имя и почта автора подставляются автоматически вне зависимости от введенных в поля.
    Нужно передать лишь текст и оценку.
    """

    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk):
        models.Review.objects.create(
            author=request.user.username,
            email=request.user.profile.email,
            text=request.data["text"],
            rate=request.data["rate"],
            date=datetime.now(),
            product_id=pk,
        )
        return Response(request.data)


class TagsListAPIView(ListAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class SalesList(ListAPIView):
    def get(self, request: Request):
        sales = models.Sale.objects.all()
        serialized = serializers.SaleSerializer(sales, many=True)
        return Response({"items": serialized.data})


class LimitedAPIView(APIView):
    def get(self, request: Request):
        products = models.Product.objects.filter(count__lt=7)[:16]
        serialized = serializers.ProductShortSerializer(products, many=True)
        return Response(serialized.data)


class PopularAPIView(APIView):
    def get(self, request: Request):
        products = models.Product.objects.filter(count__gt=0).order_by("-reviews")[:8]
        serialized = serializers.ProductShortSerializer(products, many=True)
        return Response(serialized.data)


class Banners(APIView):
    def get(self, request: Request):
        products = models.Product.objects.filter(count__gt=0).order_by("-reviews")[:3]
        serialized = serializers.ProductShortSerializer(products, many=True)
        return Response(serialized.data)


class CatalogPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        last_page_number = self.page.paginator.num_pages
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": last_page_number,
            }
        )


class Catalog(ListAPIView):
    serializer_class = serializers.ProductShortSerializer  # сериалайзер по каталог
    pagination_class = CatalogPagination  # пагинация

    def get_queryset(self):
        """
        Образец запроса.

        GET /api/catalog?

        filter[name]=&
        filter[minPrice]=0&
        filter[maxPrice]=50000&
        filter[freeDelivery]=false&
        filter[available]=true&

        currentPage=1&
        sort=date&
        sortType=dec&
        limit=20
        """
        queryset = models.Product.objects.all()
        params = self.request.query_params
        ordering = params.get("sort")
        sort_type = params.get("sortType")

        if params:
            # filter

            name = params.get("filter[name]")
            if name:
                queryset = queryset.filter(title__icontains=name)

            min_price = params.get("filter[minPrice]")
            if min_price:
                queryset = queryset.filter(price__gte=min_price)

            max_price = params.get("filter[maxPrice]")
            if max_price:
                queryset = queryset.filter(price__lte=max_price)

            free_delivery = (
                True if params.get("filter[freeDelivery]") == "true" else False
            )
            if free_delivery:
                queryset = queryset.filter(freeDelivery=True)

            available = True if params.get("filter[available]") == "true" else False
            if available:
                queryset = queryset.filter(count__gt=0)

            # sort

            if ordering == "price" and sort_type == "inc":
                queryset = queryset.order_by("price")
            elif ordering == "price" and sort_type == "dec":
                queryset = queryset.order_by("-price")

            elif ordering == "date" and sort_type == "inc":
                queryset = queryset.order_by("-date")
            elif ordering == "date" and sort_type == "dec":
                queryset = queryset.order_by("date")

            elif ordering == "reviews" and sort_type == "inc":
                queryset = queryset.order_by("-reviews")
            elif ordering == "reviews" and sort_type == "dec":
                queryset = queryset.order_by("reviews")

            elif ordering == "rating" and sort_type == "inc":
                queryset = queryset.annotate(orders_count=Count("reviews")).order_by(
                    "-orders_count"
                )
            elif ordering == "rating" and sort_type == "dec":
                queryset = queryset.annotate(orders_count=Count("reviews")).order_by(
                    "orders_count"
                )

            else:
                queryset = queryset.order_by("price")
        return queryset
