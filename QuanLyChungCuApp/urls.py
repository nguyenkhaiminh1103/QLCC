from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentViewSet, RelativeAccessViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('payments', PaymentViewSet, basename='payment')
router.register('relatives', RelativeAccessViewSet, basename='relative')

urlpatterns = [
    path('api/', include(router.urls))
]
