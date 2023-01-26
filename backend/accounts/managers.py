from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


#  이메일 회원가입을 위한 UseManager
class UserManager(BaseUserManager):
    """
        일반 유저 생성시
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 비밀번호 암호화 저장
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
            superuser 생성시
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)