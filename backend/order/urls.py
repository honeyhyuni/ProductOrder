from django.urls import path
from order import views
urlpatterns = [
    path('', views.OrderListAPIView.as_view()),
    path('<int:pk>/', views.OrderRetrieveAPIView.as_view()),
]