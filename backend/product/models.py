from django.conf import settings
from django.db import models


class TimestampedModel(models.Model):
    """
        생성일자, 수정일자 Model
    """
    created_at = models.DateTimeField('Created AT', auto_now_add=True)
    updated_at = models.DateTimeField('Updated AT', auto_now=True)

    class Meta:
        abstract = True


class Category(TimestampedModel):
    """
        카테고리 Model
    """
    name = models.CharField("Name", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리 모음'
        db_table = 'category'


class Product(TimestampedModel):
    """
        제품 Model
    """
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default="ETC", related_name='product')
    name = models.CharField("Name", max_length=50)
    photo = models.ImageField("Photo", upload_to='product/%Y/%m/%d', help_text="Require")
    price = models.PositiveIntegerField("Price", help_text="Price can't negative")
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, default=0,
                                           related_name='like_post_set')
    content = models.CharField('Content', max_length=500)
    quantity = models.PositiveIntegerField('Quantity', default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = '제품'
        verbose_name_plural = '제품 모음'
        db_table = 'product'
        ordering = ('-updated_at', '-created_at')

    def __str__(self):
        return self.name

    @property
    def like_count(self):
        return self.like_user_set.count()

