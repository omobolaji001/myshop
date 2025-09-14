from django.urls import path, include
from rest_framework import routers
from cart.api import views

app_name = 'cart'

router = routers.DefaultRouter()
router.register(r'carts', views.CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
]
