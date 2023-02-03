# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# from django.db import models
# from .services import convert
#
#
# class CouponManager(models.Manager):
#     ...
#
#     def create_coupon(self, coupon_code, end_date, **extra_fields):
#         new_coupon_code = convert()
#         while self.filter(coupon_code=new_coupon_code).exists():
#             new_coupon_code = convert()
#         end_date = datetime.now() + relativedelta(months=12)
#         coupon_code = new_coupon_code
#         coupon = self.create(copon_rules=1, coupon_code=coupon_code, end_date=end_date, **extra_fields)
#         print(coupon)
#         coupon.save()
#         return coupon
