
from django.urls import path, include

urlpatterns = [
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('', include('dj_rest_auth.urls')),  # 로그인, 로그아웃, TokenRefresh, changePassword ETC
]