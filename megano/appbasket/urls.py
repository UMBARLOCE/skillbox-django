from django.urls import path
from . import views


app_name = "appbasket"

urlpatterns = [
    path("api/basket", views.BasketAPIView.as_view(), name="basket"),
    path("api/orders", views.OrderAPIView.as_view(), name="orders"),
    path("api/order/<int:pk>", views.OrderDetailAPIView.as_view(), name="order_id"),
    path("api/payment/<int:pk>", views.PaymentAPIView.as_view(), name="payment_id"),
]
