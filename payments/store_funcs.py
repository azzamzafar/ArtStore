from store.models import Item,Cart,Invoice,Product
from customers_auth.models import Customer

def get_last_invoice(user):
    customer = Customer.objects.get(email=user)
    invoice = Invoice.objects.filter(customer=customer).order_by('id').last()
    return invoice

def set_last_invoice(customer,status):
    invoice = Invoice.objects.filter(customer=customer).order_by('id').last()
    invoice.status=status

def decrease_product_quantity(invoice):
    for order in invoice.orders.all():
        p_id = order.product_id
        prod=Product.objects.get(id=p_id)
        prod.quantity-=order.Qty
        prod.save()

def empty_cart(invoice,user):
    customer = Customer.objects.get(email=user)
    if invoice.orders.all().count()>1:
        cart  = Cart.objects.get(customer=customer)
        for item in cart.items.all():
            item.delete()
        cart.save()

    