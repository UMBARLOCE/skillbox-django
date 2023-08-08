from django.urls import path
from . import views


app_name = "appmarket"

urlpatterns = [
    path("api/categories", views.CatalogItemListAPIView.as_view(), name="categories"),
    path("api/product/<int:pk>", views.ProductDetail.as_view(), name="product_id"),
    path(
        "api/product/<int:pk>/reviews",
        views.ReviewCreateAPIView.as_view(),
        name="reviews",
    ),
    path("api/tags", views.TagsListAPIView.as_view(), name="tags"),
    path("api/sales", views.SalesList.as_view(), name="sales"),
    path("api/products/limited", views.LimitedAPIView.as_view(), name="limited"),
    path("api/products/popular", views.PopularAPIView.as_view(), name="popular"),
    path("api/catalog", views.Catalog.as_view(), name="catalog"),
    path("api/banners", views.Banners.as_view(), name="banners"),
]
