from django.contrib import admin
from .models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'photo', 'price', 'like_count', 'created_at', 'updated_at')
    list_display_links = ('name',)

    def like_count(self, obj):
        return len(obj.like_user_set.all())


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
