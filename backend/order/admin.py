from order.models import Order
from django.contrib import admin


@admin.register(Order)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'coupon', 'created_at', 'amount')
    list_display_links = ('product',)
