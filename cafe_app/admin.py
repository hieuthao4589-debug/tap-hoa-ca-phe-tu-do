from django.contrib import admin
from .models import Category, Product, ProductSize, Order, OrderDetail

admin.site.register(Category)

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline]
    list_display = ['name', 'price', 'category']

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderDetail)