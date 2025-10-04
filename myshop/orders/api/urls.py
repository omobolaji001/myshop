from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.api.views import OrderViewSet

app_name = 'orders'

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
]
