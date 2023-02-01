from django.contrib import admin
from store.models import Product,Category,Cart,Invoice

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','amount')

# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Invoice)
admin.site.register(Cart)