from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Sum
from django.views.generic import DetailView, FormView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.decorators import login_required
from store.forms import ItemsForm
from store.models import Cart, Invoice, Item, Order, Product
from customers_auth.models import Customer

# Create your views here.
class ProductListView(MultipleObjectMixin, FormView):
    queryset = Product.objects.order_by("amount")
    object_list = queryset
    # context_object_name = "Product_list"
    paginate_by: int = 9
    template_name = "store/home.html"
    form_class = ItemsForm

    def get_success_url(self):
        if self.request.POST.get('action')=='item':
            return redirect(self.request.path_info)
        elif self.request.POST.get('action')=='order':
            return reverse('profile')

    def form_valid(self,form):
        user = Customer.objects.filter(email=self.request.user)[0]

        if self.request.POST.get("action") == "item":
            cart_obj = Cart.objects.get_or_create(customer=user)[0]
            product_id = form.cleaned_data.get("prod_id")
            prod_obj = Product.objects.filter(id=product_id)[0]
            price = prod_obj.amount
            item_obj = Item.objects.create(
                product=prod_obj,
                price=price,
                Qty=form.cleaned_data.get("Qty"),
                cart=cart_obj,
            )
            item_obj.save()
            
        elif self.request.POST.get("action") == "order":
            if self.request.user.is_anonymous:
                return redirect("login")
            elif not user.address1:
                return reverse("profile")
            invoice_obj = Invoice.objects.get_or_create(customer=user)[0]
            product_id = form.cleaned_data.get("prod_id")
            prod_obj = Product.objects.filter(id=product_id)[0]
            price = prod_obj.amount
            order_obj = Order.objects.create(
                product=prod_obj,
                price=price,
                Qty=form.cleaned_data.get("Qty"),
                invoice=invoice_obj,
            )
            order_obj.save()
        return self.get_success_url()

    def form_invalid(self, form):
        return super().form_invalid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ItemsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ItemsForm(request.POST)
        if form.is_valid():
            return self.form_valid(form) 
        else:
            return self.form_invalid(form)
        
        


class ProductDetailView(DetailView):
    model = Product
    template_name: str = "store/product-detail.html"

@login_required(login_url='login')
def cartview(request):
    my_cart = Cart.objects.get_or_create(customer=request.user)[0]
    if Item.objects.filter(cart=my_cart):
        my_cart.cart_Qty = Item.objects.filter(cart=my_cart).aggregate(Sum("Qty")).get("Qty__sum")
        my_cart.cart_total = Item.objects.filter(cart=my_cart).aggregate(Sum("order_amount")).get("order_amount__sum")
        my_items = my_cart.user_items.all()
    return render(
        request,
        "store/cart.html",
        {"total": my_cart.cart_total, "Qty": my_cart.cart_Qty, "my_items": my_items},
    )

@login_required(login_url='login')
def orderview(request):
    if not Invoice.objects.filter(customer=request.user):
        
        return render(request,'store/order-summary.html',{'total':None,'Qty':None,'my_orders':None})
    else:

        my_invoice = Invoice.objects.filter(customer=request.user)[0]
        my_invoice.total_amount = Order.objects.filter(invoice=my_invoice).aggregate(Sum('order_amount')).get('order_amount__sum')
        my_invoice.total_Qty = Order.objects.filter(invoice=my_invoice).aggregate(Sum('Qty')).get('Qty__sum')
        my_orders = my_invoice.user_orders.all()
    return render(request,{'total':my_invoice.total_amount,'Qty':my_invoice.total_Qty,'my_orders':my_orders})

# def cart(request):

#     return render(request)
# Function List View with Pagination
# def home(request):

#     Products = Product.objects.all()
#     # print(Products.values_list('name',flat=True)[0])
#     paginator = Paginator(Products,9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'store/home.html',{'page_obj':page_obj})
