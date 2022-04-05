from accounts.models import Account
from django.db import models
from store.models import Product, Variation

# Create your models here.


class Payment(models.Model):
    # ForeignKey Fields
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # ...

    # Main Fields
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    # this is the total amount paid
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    # ...

    # Helpers
    created_at = models.DateTimeField(auto_now_add=True)
    # ...

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    # ForeignKey Fields
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    # ...

    # User Info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    # ...

    # Address
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    # ...

    # Order info
    order_number = models.CharField(max_length=20)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    # ...

    # Helpers
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ...

    def __str__(self):
        return self.first_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'


class OrderProduct(models.Model):
    # ForeignKey Fields
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # ...

    # Many to Many Fields
    variations = models.ManyToManyField(Variation, blank=True)
    # ...

    # Main Fields
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    # ...

    # Helpers
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ...

    def __str__(self):
        return self.product.product_name
