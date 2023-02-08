from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('product.urls')),
    path('coupon/', include('coupon.urls')),
    path('order/', include('order.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)