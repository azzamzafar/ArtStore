from django.contrib import admin
from store.models import Product,Category,Order,Cart

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','amount')

# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Cart)