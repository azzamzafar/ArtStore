from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
# from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
# from django.contrib.contenttypes.models import ContentType

# Create your models here.
# User = get_user_model()


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
    amount = models.PositiveIntegerField()


class Invoice(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="invoice"
    )
    total_amount = models.PositiveIntegerField(null=True)
    total_Qty = models.PositiveSmallIntegerField(null=True)
    date = models.DateField(auto_now_add=True)
    shipping_address = models.TextField(null=True)

    def save(self, *args, **kwargs):
        self.shipping_address = self.customer.address1 + " " + self.customer.address2
        super(Invoice, self).save(*args, **kwargs)


class Cart(models.Model):
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    total_amount = models.PositiveIntegerField(null=True)
    total_Qty = models.PositiveSmallIntegerField(null=True)

class Order(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="prod_orders", null=True
    )
    price = models.PositiveIntegerField(default=0)
    order_amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=4)
    Qty = models.PositiveIntegerField(default=0)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="user_orders", null=True
    )

    def save(self, *args, **kwargs):
        self.price = self.product.price
        total_price = self.price * self.Qty
        self.order_amount = total_price
        self.currency = "INR"
        super(Order, self).save(*args, **kwargs)


class Item(models.Model):
   
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="cart_items", null=True
    )
    price = models.PositiveIntegerField(default=0)
    order_amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=4)
    Qty = models.PositiveIntegerField(default=0)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="user_items", null=True
    )

    def save(self, *args, **kwargs):
        self.price = self.product.amount
        total_price = self.price * self.Qty
        self.order_amount = total_price
        self.currency = "INR"
        super(Item, self).save(*args, **kwargs)