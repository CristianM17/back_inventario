from django.contrib import admin
from django.urls import path
from .views import (
    ProductosBajoStockAPIView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('estadisticas/', ProductosBajoStockAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]