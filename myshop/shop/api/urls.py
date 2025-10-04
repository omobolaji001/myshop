from django.urls import path, include
from rest_framework import routers
from shop.api import views

app_name = 'shop'

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]
