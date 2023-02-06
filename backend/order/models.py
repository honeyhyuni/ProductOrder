from django.conf import settings
from django.db import models

from product.models import Product
from coupon.models import UserCoupon


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default='secession user',
                             related_name='user_order')
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default='remove product',
                                related_name='product_order')
    coupon = models.ForeignKey(UserCoupon, on_delete=models.SET_DEFAULT, null=True, default='', related_name='coupon_order')
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()

    objects = models.Manager()

    class Meta:
        verbose_name = '주문 내역'
        verbose_name_plural = '주문 내역 모음'
        db_table = 'order'
