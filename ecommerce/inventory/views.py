from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import StockMovement, LowStockAlert
from cart.models import Product
from .serializers import StockMovementSerializer, LowStockAlertSerializer, ProductSerializer

# API for Stock Movements
class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

# API for Low Stock Alerts
class LowStockAlertViewSet(viewsets.ModelViewSet):
    queryset = LowStockAlert.objects.all()
    serializer_class = LowStockAlertSerializer

# API for Products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset
