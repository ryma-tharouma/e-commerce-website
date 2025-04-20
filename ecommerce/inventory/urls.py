from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockMovementViewSet, LowStockAlertViewSet, ProductViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'stock-movements', StockMovementViewSet, basename='stock-movements')
router.register(r'low-stock-alerts', LowStockAlertViewSet, basename='low-stock-alerts')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('api/', include(router.urls)),  # Include the API routes
]