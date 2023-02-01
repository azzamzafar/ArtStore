from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Category(models.Model):
    value = models.CharField(_("category"), max_length=100)

    def __str__(self):
        return str(self.value)


class Product(models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), max_length=500)
    available = models.BooleanField()
    quantity = models.PositiveSmallIntegerField()
    category = models.ManyToManyField(Category, related_name="products")
    photo = models.ImageField(upload_to = 'products')
    amount = models.PositiveIntegerField()

class Item(models.Model):
   
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="items", null=True
    )
    price = models.PositiveIntegerField(default=0)
    order_amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=4)
    Qty = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.price = self.product.amount
        total_price = self.price * self.Qty
        self.order_amount = total_price
        self.currency = "INR"
        super(Item, self).save(*args, **kwargs)

class   Order(models.Model):
   
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders", null=True
    )
    price = models.PositiveIntegerField(default=0)
    order_amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=4)
    Qty = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.price = self.product.amount
        total_price = self.price * self.Qty
        self.order_amount = total_price
        self.currency = "INR"
        super(Order, self).save(*args, **kwargs)

class Invoice(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="invoice"
        )
    total_amount = models.PositiveIntegerField(default=0)
    total_Qty = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15,null=True)
    shipping_address = models.TextField(null=True)
    orders = models.ManyToManyField(Order,related_name='orders_invoice')
    def save(self,*args,**kwargs):
        super(Invoice, self).save(*args, **kwargs)
        if self.orders.exists():
            self.total_amount = self.orders.all().aggregate(models.Sum('order_amount')).get('order_amount__sum')
            self.total_Qty = self.orders.all().aggregate(models.Sum('Qty')).get('Qty__sum')
            super(Invoice, self).save(*args, **kwargs) 
        elif self.total_amount!=0 and self.total_Qty!=0:
            self.total_amount=0
            self.total_Qty=0
            super(Invoice, self).save(*args, **kwargs)
        if self.customer.address1 and self.customer.address2:
            self.shipping_address=self.customer.address1+" "+self.customer.address2
            super(Invoice, self).save(*args, **kwargs)
        elif self.shipping_address is not None:
            self.shipping_address=None
            super(Invoice, self).save(*args, **kwargs)

class Cart(models.Model):
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    total_amount = models.PositiveIntegerField(default=0)
    total_Qty = models.PositiveSmallIntegerField(default=0)
    items = models.ManyToManyField(Item,related_name='items_cart')
    def save(self,*args,**kwargs):
        super(Cart, self).save(*args, **kwargs)
        if self.items.exists():
            self.total_amount = self.items.all().aggregate(models.Sum('order_amount')).get('order_amount__sum')
            self.total_Qty = self.items.all().aggregate(models.Sum('Qty')).get('Qty__sum')
            super(Cart, self).save(*args, **kwargs)
        elif self.total_amount!=0 and self.total_Qty!=0:
            self.total_amount=0
            self.total_Qty=0
            super(Cart,self).save(*args,**kwargs)
