from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductAPIView, TestView

router = DefaultRouter()
router.register('product', ProductAPIView, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('product/<int:pk>/order/', TestView.as_view())
]
