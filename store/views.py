from django.shortcuts import render,redirect
from .models import Product
# Create your views here.
def home(request):
    
    Products = Product.objects.all()
    # print(Products.values_list('name',flat=True)[0])
    if len(Products)>9:
        Products = Product.objects.all()[:9]
    return render(request,'store/home.html',{'Products':Products,'range':range(3)}) 