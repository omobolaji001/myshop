from django.urls import path, include
from rest_framework import routers
from .views import CartViewSet

app_name = 'cart'

router = routers.DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
]
