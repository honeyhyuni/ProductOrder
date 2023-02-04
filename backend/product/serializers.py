from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product


class GetLoginProductSerializers(serializers.ModelSerializer):
    """
        GET Serializer IS Authenticated
    """
    is_like = serializers.SerializerMethodField('is_like_field')

    # True is already Like, False is None Like
    def is_like_field(self, product):
        if 'login' in self.context:
            user = self.context['request'].user
            return product.like_user_set.filter(pk=user.pk).exists()
        return False

    class Meta:
        model = Product
        fields = (
            'name', 'category', 'content', 'price', 'photo', 'created_at', 'updated_at', 'quantity', 'like_count',
            'is_like')


class GetProductSerializers(serializers.ModelSerializer):
    """
        GET Serializer IS NOT Authenticated
    """

    class Meta:
        model = Product
        fields = (
            'name', 'category', 'content', 'price', 'photo', 'created_at', 'updated_at', 'quantity', 'like_count',)


class NGetProductSerializers(serializers.ModelSerializer):
    """
        POST, PATCH, PUT Serializer
    """

    class Meta:
        model = Product
        fields = ('name', 'category', 'content', 'price', 'photo', 'created_at', 'updated_at', 'quantity',)

    def validate_price(self, value):
        if 1000 > value:
            raise ValidationError('1000원 미만의 상품은 등록할수 없습니다.')
        return value

    def validate_quantity(self, value):
        if 10 > value:
            raise ValidationError('상품은 10개 이상부터 등록 가능합니다.')
        return value

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.content = validated_data.get('content', instance.content)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance
