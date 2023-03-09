import re
from rest_framework.exceptions import ValidationError
from .models import User
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    """
        회원가입 Serializer
    """
    check_password = serializers.CharField(style={'input_type': 'password'}, write_only=True
                                           , required=True)
    name = serializers.CharField(source='name')

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'check_password')
        extra_kwargs = {
            'name': {'write_only': True},
            'password': {'write_only': True},
            'check_password': {'write_only': True},
        }

    """
        유효성 검사
    """

    def validate_password(self, value):
        if not re.search(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,15}$', value):
            raise ValidationError('비밀번호는 8글자 이상, 15글자 이하이며 특수문자, 숫자를 포함해야 합니다.')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        check_password = attrs.get('check_password')
        if password != check_password:
            raise ValidationError('입력된 두 비밀번호가 다릅니다.')
        return attrs

    """
        create User
        비밀번호를 체크하기위한 check_password 필드는 
        제외하고 저장한다.
    """

    def create(self, validated_data):
        validated_data.pop('check_password')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    """
        Login Serializer
    """

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }
