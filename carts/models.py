from accounts.models import Account
from django.db import models
from store.models import Product, Variation

# Create your models here.


class Cart(models.Model):
    # Info about Cart
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    # ...

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    # ForeignKey Fields
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    # ...

    # Many to Many Fields
    variations = models.ManyToManyField(Variation, blank=True)
    # ...

    # Main Fields
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    # ...

    def __unicode__(self):
        return self.product

    def sub_total(self):
        return self.product.price * self.quantity
