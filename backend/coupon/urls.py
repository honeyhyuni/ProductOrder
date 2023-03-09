from django.urls import path
from .views import CreateListCoupon, AllCouponRulesList, UserCouponAPIView
urlpatterns=[
    path('', CreateListCoupon.as_view(), name='coupon'),
    path('coupon_rules/', AllCouponRulesList.as_view(), name='couponRules-all'),
    path('user/', UserCouponAPIView.as_view(), name='userCoupon'),
]