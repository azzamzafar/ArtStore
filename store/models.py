from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
# from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Category(models.Model):
    value = models.CharField(_("category"),max_length=100)
    def __str__(self):
        return str(self.value)

class Product(models.Model):
    name = models.CharField(_("name"),max_length=50)
    description = models.TextField(_("description"),max_length=500)
    available = models.BooleanField()
    quantity = models.PositiveSmallIntegerField()
    category = models.ManyToManyField(Category,related_name='products')
    amount = models.PositiveIntegerField()
    # Generic Foreign Key 
    # object_id = models.PositiveIntegerField()
    # content_type = models.ForeignKey(ContentType, on_delete=models.RESTRICT)
    # content_object = GenericForeignKey("content_type","object_id")

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,related_name='order')
    product = models.ForeignKey(Product,on_delete=models.RESTRICT,related_name='orders',null=True)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=4)

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,related_name='cart') 
    items = models.ForeignKey(Product,on_delete=models.RESTRICT,related_name='carts',null=True)
    quantity = models.IntegerField(editable=True,default=0)