from datetime import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from .models import Coupon, CouponRules, UserCoupon
from .services import convert


class CouponRulesBaseSerializers(serializers.ModelSerializer):
    """
        CouponRules Base Serializers
    """

    class Meta:
        model = CouponRules
        fields = '__all__'
        depth = 3


class CouponBaseSerializers(serializers.ModelSerializer):
    """
        Coupon Base Serializers
    """

    class Meta:
        model = Coupon
        fields = '__all__'


class UserCouponBaseSerializers(serializers.ModelSerializer):
    """
        UserCoupon Base Serializers
    """

    class Meta:
        model = UserCoupon
        fields = '__all__'


class CouponListCreateSerializers(serializers.ModelSerializer):
    """
        Only Coupon Create List API Serializers
    """
    active = serializers.BooleanField(default=True)
    end_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
            Random 한 10~15 자릿수 문자열 쿠폰 코드 등록
        """
        new_coupon_code = convert()
        while Coupon.objects.filter(coupon_code=new_coupon_code).exists():
            new_coupon_code = convert()
        coupon_code = new_coupon_code
        end_date = datetime.now() + relativedelta(months=12)
        coupon = Coupon.objects.create(end_date=end_date, coupon_code=coupon_code, **validated_data)
        return coupon

    class Meta:
        model = Coupon
        fields = ('id', 'coupon_rules', 'coupon_code', 'start_date', 'end_date', 'active')


class CouponRuleListSerializers(serializers.Serializer):
    """
        All CouponRules : Return -> List
    """
    couponRulesList = serializers.ListSerializer(child=serializers.CharField())


class UserCouponListSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    coupon = serializers.StringRelatedField()

    class Meta:
        model = UserCoupon
        fields = ('user', 'status', 'coupon',)
        read_only_fields = ('status',)


class CreateUserCouponSerializers(serializers.Serializer):
    coupon_rules = CouponRulesBaseSerializers()
    coupon = CouponBaseSerializers()


