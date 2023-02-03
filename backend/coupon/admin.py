from django.contrib import admin
from .models import Coupon, CouponRules, UserCoupon


@admin.register(CouponRules)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_name', 'discount_policy', 'discount', 'created_at',)
    list_display_links = ('coupon_name',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_rules', 'coupon_code', 'start_date', 'end_date', 'active')
    list_display_links = ('coupon_code',)


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'status',)
    list_display_links = ('coupon',)
