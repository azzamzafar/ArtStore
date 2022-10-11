from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Product
# from django.core.paginator import Paginator
# Create your views here.


class ProductListView(ListView):
    queryset = Product.objects.order_by('amount')
    paginate_by: int = 9
    template_name = "store/home.html"

class ProductDetailView(DetailView):
    model = Product
    template_name: str = "store/product-detail.html"

# Function List View with Pagination
# def home(request):
    
#     Products = Product.objects.all()
#     # print(Products.values_list('name',flat=True)[0])
#     paginator = Paginator(Products,9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'store/home.html',{'page_obj':page_obj})