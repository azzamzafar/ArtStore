from django import forms
from django.contrib import admin
from store.models import Product,Category,Cart,Invoice


class ProductAdminForm(forms.ModelForm):
    photo = forms.FileField()
    class Meta:
        model=Product
        exclude = ("photo",)
    
    def save(self,commit=True):
        super(ProductAdminForm,self).save(commit=False)
        if self.cleaned_data.get('photo') is not None \
            and hasattr(self.cleaned_data['photo'],'file'):
            data = self.cleaned_data['photo'].file.read()
            self.instance.photo = data      
            super(ProductAdminForm,self).save()
        
        return self.instance
    
    def save_m2m(self):
        ...

class ProductAdmin(admin.ModelAdmin):
    form=ProductAdminForm
    list_display = ('name','amount','photo_tag',)


# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Invoice)
admin.site.register(Cart)