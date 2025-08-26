from django.urls import path, include
from rest_framework import routers
from shop.api import views


router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]
