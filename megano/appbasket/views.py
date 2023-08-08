from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .cart import Basket
from .serializers import OrderSerializer
from .models import Order, OrderProducts
from appmarket.models import Product


class BasketAPIView(APIView):
    def get(self, request):
        basket = Basket(request)
        return Response(data=basket.get())

    def post(self, request):
        basket = Basket(request)
        basket.add()
        return Response(data=basket.get())

    def delete(self, request):
        basket = Basket(request)
        basket.remove()
        return Response(data=basket.get())


class OrderAPIView(APIView):
    def get(self, request):
        orders = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("products")
            .select_related("user")
        )
        serialized = OrderSerializer(orders, many=True)
        return Response(data=serialized.data)

    def post(self, request):
        data = request.data
        order = Order.objects.create(user=request.user)
        total_cost = 0
        for product_data in data:
            product = Product.objects.get(pk=product_data.get("id"))
            count = min(product.count, int(product_data.get("count")))
            query = OrderProducts.objects.create(
                count=count, order=order, product=product
            )
            product.count -= count
            total_cost += product.price * count
            query.save()
            product.save()
        order.status = "created"
        order.totalCost = total_cost
        order.save()
        basket = Basket(request)
        basket.clear()
        return Response(data={"orderId": order.id})


class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        serialized = OrderSerializer(order)
        return Response(data=serialized.data)

    def post(self, request, pk):
        data = request.data
        serialized = OrderSerializer(data=data)
        if serialized.is_valid():
            order = Order.objects.get(pk=data.get("orderId"))
            validated_data = serialized.validated_data
            serialized.update(order, validated_data)
            delivery_type = "ordinary"
            if not order.deliveryType:
                order.deliveryType = delivery_type = "ordinary"
            if order.totalCost < 50:
                order.totalCost += 10
            if delivery_type == "express":
                order.totalCost += 20
            order.status = "not paid"
            order.save()
            return Response(data={"orderId": order.id})
        return Response(status=400)


class PaymentAPIView(APIView):
    def post(self, request: Request, pk):
        order = Order.objects.get(pk=pk)
        order.status = "paid"
        order.save()
        return Response(request.data, status=status.HTTP_200_OK)
