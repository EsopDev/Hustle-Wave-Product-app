from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
 

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)