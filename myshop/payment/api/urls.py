from django.urls import path, include
from payment.api.views import PaymentViewSet
from rest_framework.routers import DefaultRouter

app_name = 'payment'

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')


urlpatterns = [
    path('', include(router.urls)),
]
