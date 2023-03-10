from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from store.forms import ItemsForm
from store.models import Cart, Invoice, Item, Product,Order
from customers_auth.models import Customer
      
class ProductListView(ListView):
    queryset = Product.objects.order_by("amount")
    object_list = queryset
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
    
    def form_valid(self,form):
        
        user = Customer.objects.filter(email=self.request.user)[0]
        if self.request.POST.get("action") == "item":
            cart,created = Cart.objects.get_or_create(customer=user)
            p_id = form.cleaned_data.get("prod_id")
            Qty = form.cleaned_data.get('Qty')
            prod = Product.objects.get(id=p_id)
            if Qty>prod.quantity:
                messages.add_message(self.request,messages.ERROR,'Requested Qty not allowed') 
                return redirect(self.request.path_info)
            elif p_id not in cart.items.values_list('product_id',flat=True):
                item = Item.objects.create(
                    product=prod,
                    Qty=Qty)
                cart.items.add(item)
                cart.save()
            else:
                messages.add_message(self.request,messages.INFO,"Item is already present in your Cart!")
                return redirect(self.request.path_info)
                

        elif self.request.POST.get("action") == "order":
           
            if user.address1 is None:
                return redirect("profile")
            invoice = Invoice.objects.create(customer=user)
            p_id = form.cleaned_data.get("prod_id")
            Qty = form.cleaned_data.get('Qty')
            prod = Product.objects.get(id=p_id)
            if Qty<=prod.quantity:
                order = Order.objects.create(
                    product=prod,
                    Qty=Qty)
                invoice.orders.add(order)
                invoice.save()
            else:
                messages.add_message(self.request,messages.ERROR,'Requested Qty not allowed') 
                return redirect(self.request.path_info)
        return self.get_success_url()
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    
    def post(self,request,*args,**kwargs):
        if self.request.user.is_anonymous:
            return redirect(reverse('login'))
        form = ItemsForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required(login_url='login')
def cartview(request):
    customer = Customer.objects.get(email=request.user)
    cart = Cart.objects.get_or_create(customer=customer)[0]
    my_items=None
    if cart.items.exists():
        my_items = cart.items.all()

        if request.method=='POST':
            
            if request.POST.get('action')=='remove-all':
                for item in Item.objects.filter(cart=cart):
                    item.delete()
                cart.total_amount = 0
                cart.total_Qty = 0
            elif request.POST.get('action')=='remove-item':
                item_id = request.POST.get('item_id')
                item = Item.objects.filter(id=item_id)[0]
                cart.items.remove(item)
                cart.save()
                item.delete()
            elif request.POST.get('action')=='checkout':
                
                if customer.address1 is None:
                    return redirect('profile')
                else:
                    invoice = Invoice.objects.create(customer=customer)
                    for item in my_items:
                        prod = Product.objects.get(id=item.product_id)
                        qty = item.Qty
                        order = Order.objects.create(
                            product=prod,
                            Qty=qty)
                        invoice.orders.add(order)
                    invoice.save()
                    return redirect('cart-order')
            elif request.POST.get('action')=="increase":
                ...
                item_id = request.POST.get('item_id')
                item = Item.objects.filter(id=item_id)[0]
                item.Qty+=1
                item.save()
                cart.save()
            elif request.POST.get('action')=="decrease":
                item_id = request.POST.get('item_id')
                item = Item.objects.filter(id=item_id)[0]
                item.Qty-=1
                item.save()
                cart.save()


    return render(
        request,
        "store/cart.html",
        {"total": cart.total_amount, "Qty": cart.total_Qty, "my_items": my_items},
    )

def cart_order(request):
    invoice = Invoice.objects.filter(customer=request.user).order_by('id').latest('id')
    print(invoice)
    print(invoice.total_amount)
    my_orders = invoice.orders.all()
    
    return render(request,'store/cart-order.html',{'my_orders':my_orders,'total':invoice.total_amount,'Qty':invoice.total_Qty})
  
class ProductCategoryView(ListView):
    paginate_by: int = 9
    template_name = "store/category.html"
    queryset=None
    def get_queryset(self):
        print(Product.objects.filter(category__slug=self.kwargs.get('slug')).order_by('amount'))
        return Product.objects.filter(category__slug=self.kwargs['slug']).order_by('amount')
    object_list=queryset
