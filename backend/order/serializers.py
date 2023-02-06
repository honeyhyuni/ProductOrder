from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    coupon = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ('user', 'product', 'coupon', 'amount',)

    def create(self, validated_data):
        product = self.context['product']
        coupon = self.context['coupon']
        user = self.context['user']
        user_quantity = self.context['user_quantity']
        order = Order.objects.create(product=product, coupon=coupon, user=user, **validated_data)
        product.quantity -= user_quantity
        product.save()
        if coupon is not None:
            coupon.status = False
            coupon.save()
        return order
