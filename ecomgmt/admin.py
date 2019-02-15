from django.contrib import admin
from models import *


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_no',)
    ordering = ('sort_no',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_no',)
    list_filter = ('supplier', 'type')

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
