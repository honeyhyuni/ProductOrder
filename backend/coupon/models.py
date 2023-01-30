from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.core.validators import ValidationError
from .services import convert


class TimestampedModel(models.Model):
    """
        생성일자, 수정일자 Model
    """
    created_at = models.DateTimeField('Created AT', auto_now_add=True)
    updated_at = models.DateTimeField('Updated AT', auto_now=True)

    class Meta:
        abstract = True


class CouponRules(TimestampedModel):
    """
        쿠폰 BASE Model
    """
    Percent_discount = 'PD'
    FlatRate_discount = 'FD'
    Discount_Choice = [
        (Percent_discount, 'Percent'),
        (FlatRate_discount, 'FlatRate'),
    ]

    coupon_name = models.CharField("Name", max_length=100)
    discount_policy = models.CharField("Discount Policy",
                                       max_length=2,
                                       choices=Discount_Choice,
                                       default=FlatRate_discount,
                                       )
    discount = models.PositiveIntegerField("Discount", help_text='if select PD 5%~100%, else 1000~50000')

    def clean(self):
        """
            유효성 검사
        """
        discount_policy = self.discount_policy
        discount = self.discount
        if discount_policy == 'PD' and (discount % 5 != 0 or not (5 <= discount <= 100)):
            raise ValidationError("%할인은 5의배수이면서 100 이하입니다")
        elif discount_policy == 'FD' and (discount % 5000 != 0 or not (5000 <= discount <= 50000)):
            raise ValidationError("정액할인은 5000 배수이면서 50000원 이하입니다.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['discount_policy', 'discount'], name='Base coupon is only one')
        ]
        verbose_name = '쿠폰 베이스'
        verbose_name_plural = '쿠폰 베이스 모음'
        db_table = 'coupon_rules'
        ordering = ('-created_at',)

    def __str__(self):
        return self.coupon_name


class Coupon(models.Model):
    """
        등록된 쿠폰 Model
    """
    coupon_rules = models.ForeignKey(CouponRules, on_delete=models.CASCADE, related_name='coupon')
    coupon_code = models.CharField("Coupon Code", max_length=15, unique=True,
                                   help_text='only between 10 and 15 of characters',
                                   editable=False)
    start_date = models.DateTimeField('Start DT', auto_now_add=True)
    end_date = models.DateTimeField('End DT', null=True, blank=True)
    active = models.BooleanField("active", default=True, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = '등록된 쿠폰'
        verbose_name_plural = '등록된 쿠폰 모음'
        db_table = 'coupon'
        ordering = ('-start_date',)

    def __str__(self):
        return f"{self.coupon_code[:10]}"


class UserCoupon(TimestampedModel):
    """
        User 에게 부여된 쿠폰
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, related_name='coupon')
    status = models.BooleanField('Status', null=True, default=True)

    class Meta:
        verbose_name = '유저-쿠폰'
        verbose_name_plural = '유저-쿠폰 모음'
        db_table = 'user_coupon'

    def __str__(self):
        return f"{self.user, self.coupon}"