from django.urls import path
from .views import CreateListCoupon, AllCouponRulesList, UserCouponAPIView
urlpatterns=[
    path('coupon/', CreateListCoupon.as_view(), name='coupon'),
    path('couponRules/', AllCouponRulesList.as_view(), name='couponRules-all'),
    path('user/', UserCouponAPIView.as_view(), name='userCoupon'),
]