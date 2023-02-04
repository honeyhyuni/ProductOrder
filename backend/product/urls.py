from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductAPIView

router = DefaultRouter()
router.register('product', ProductAPIView, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
