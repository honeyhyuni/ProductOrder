from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CouponRules


class CouponRulesAllAPIViewTestCase(APITestCase):
    """
        GET couponRules-all Test
    """
    def setUp(self):
        self.data = {'coupon_name': '5000원할인', 'discount_policy': 'PD', 'discount': 5000}
        self.coupon = CouponRules.objects.create(coupon_name='5000원할인', discount_policy='PD', discount=5000)

    def test_registration(self):
        response = self.client.get(reverse('couponRules-all'), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['couponRulesList']), 1)
        self.assertEqual(response.data['couponRulesList'][0], '5000원할인')
