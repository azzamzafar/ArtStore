from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Sum
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from store.forms import ItemsForm
from store.models import Cart, Invoice, Item, Order, Product
from customers_auth.models import Customer

# Create your views here.
# class ProductListView(MultipleObjectMixin, FormView):
#     queryset = Product.objects.order_by("amount")
#     object_list = queryset
#     # context_object_name = "Product_list"
#     paginate_by: int = 9
#     template_name = "store/home.html"
#     form_class = ItemsForm

#     def get_success_url(self):
#         if self.request.POST.get('action')=='item':
#             return redirect(self.request.path_info)
#         elif self.request.POST.get('action')=='order':
#             return redirect('profile')

#     def form_valid(self,form):

#         if self.request.user.is_anonymous:
#             return redirect('login')
#         user = Customer.objects.filter(email=self.request.user)[0]
#         if self.request.POST.get("action") == "item":
#             cart_obj = Cart.objects.get_or_create(customer=self.request.user)[0]
#             product_id = form.cleaned_data.get("prod_id")
#             prod_obj = Product.objects.filter(id=product_id)[0]
#             price = prod_obj.amount
#             item_obj = Item.objects.create(
#                 product=prod_obj,
#                 price=price,
#                 Qty=form.cleaned_data.get("Qty"),
#                 cart=cart_obj,
#             )
#             item_obj.save()
#             cart_obj.other_fields()
#         elif self.request.POST.get("action") == "order":
            
#             if user.address1 is None:
#                 return reverse("profile")
#             invoice_obj = Invoice.objects.get_or_create(customer=self.request.user)[0]
#             product_id = form.cleaned_data.get("prod_id")
#             prod_obj = Product.objects.filter(id=product_id)[0]
#             price = prod_obj.amount
#             order_obj = Order.objects.create(
#                 product=prod_obj,
#                 price=price,
#                 Qty=form.cleaned_data.get("Qty"),
#                 invoice=invoice_obj,
#             )
#             order_obj.save()
#         return self.get_success_url()

#     def form_invalid(self, form):
#         return super().form_invalid(form)
    

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form"] = ItemsForm()
#         return context
    

#     def post(self, request, *args, **kwargs):
#         form = ItemsForm(request.POST)
#         if form.is_valid():
#             return self.form_valid(form) 
#         else:
#             return self.form_invalid(form)
      
class ProductListView(ListView):
    queryset = Product.objects.order_by("amount")
    object_list = queryset
    # context_object_name = "Product_list"
    paginate_by: int = 9
    template_name = "store/home.html"

class ProductDetailView(FormMixin,DetailView):
    model = Product
    form_class = ItemsForm
    template_name='store/product-detail.html'
    
    def get_success_url(self):
        if self.request.POST.get('action')=='item':
            return redirect(self.request.path_info)
        elif self.request.POST.get('action')=='order':
            return redirect('cart-order')

    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            redirect('login')
        form = ItemsForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def form_valid(self,form):
        
        user = Customer.objects.filter(email=self.request.user)[0]
        if self.request.POST.get("action") == "item":
            cart_obj = Cart.objects.get_or_create(customer=self.request.user)[0]
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
            cart_obj.other_fields()
        elif self.request.POST.get("action") == "order":
           
            if user.address1 is None:
                return redirect("profile")
            invoice_obj = Invoice.objects.create(customer=self.request.user)
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
            invoice_obj.other_fields()
        return self.get_success_url()


@login_required(login_url='login')
def cartview(request):
    my_cart = Cart.objects.get_or_create(customer=request.user)[0]
    my_cart.other_fields()
    my_items=None
    if my_cart.user_items:
        # my_cart.cart_Qty = Item.objects.filter(cart=my_cart).aggregate(Sum("Qty")).get("Qty__sum")
        # my_cart.cart_total = Item.objects.filter(cart=my_cart).aggregate(Sum("order_amount")).get("order_amount__sum")
        my_items = my_cart.user_items.all()

        if request.method=='POST':
            
            if request.POST.get('action')=='remove-all':
                for item in Item.objects.filter(cart=my_cart):
                    item.delete()
            elif request.POST.get('action')=='remove-item':
                item_id = request.POST.get('item_id')
                item = Item.objects.filter(id=item_id)[0]
                item.delete()
            elif request.POST.get('action')=='checkout':
                
                if Customer.objects.filter(email=request.user)[0].address1 is None:
                    return redirect('profile')
                else:
                    my_invoice = Invoice.objects.create(customer=request.user)
                    qty_sum=0
                    amount_sum=0
                    for item in my_items:
                        product = Product.objects.filter(id=item.product.id)[0]
                        Order.objects.create(
                            product = product,
                            Qty = item.Qty,
                            invoice = my_invoice 
                        )
                        # qty_sum+=item.Qty
                        # amount_sum+=item.order_amount
                    # my_invoice.total_Qty = qty_sum
                    # my_invoice.total_amount = amount_sum
                    my_invoice.other_fields()
                    return redirect('cart-order')
    return render(
        request,
        "store/cart.html",
        {"total": my_cart.total_amount, "Qty": my_cart.total_Qty, "my_items": my_items},
    )

def cart_order(request):
    my_invoice = Invoice.objects.filter(customer=request.user).order_by('id').latest('id')
    my_invoice.other_fields()
    print(my_invoice)
    print(my_invoice.total_amount)
    my_orders = my_invoice.user_orders.all()
    
    return render(request,'store/cart-order.html',{'my_orders':my_orders,'total':my_invoice.total_amount,'Qty':my_invoice.total_Qty})

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
