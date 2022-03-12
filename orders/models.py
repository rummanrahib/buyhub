from accounts.models import Account
from django.db import models
from store.models import Product, Variation

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, on_delete=models.CASCADE, on_delete=models.CASCADE, on_delete=models.CASCADE)

    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    # this is the total amount paid
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    # Defaults
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)

    # User Info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)

    # Address
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    # Others
    order_number = models.CharField(max_length=20)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)

    # Boolean fields
    is_ordered = models.BooleanField(default=False)
    ordered_at = models.DateTimeField(blank=True, null=True)

    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)

    is_refunded = models.BooleanField(default=False)
    refunded_at = models.DateTimeField(blank=True, null=True)
    refunded_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    refunded_ip = models.CharField(blank=True, max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'

    def get_subtotal(self):
        from django.db.models import F

        # self.orderproducts_set.all().select_related('product', 'product_images')
        # self.product.prefetch_related('order_products')
        # 0.002 sec

        subtotal = 0

        for i in self.orderproducts_set.all().only('product_price', 'quantity'):
            subtotal += i.product_price * i.quantity
            order_product > product > image

            order_product > product > image

            order_product > product > image

            order_product > product > image
            # 1 sec

        return self.order_products.aggregate(subtotal=F('product_price') * F('quantity'))['subtotal']

    def get_order_number(self):
        import datetime
        year = int(datetime.date.today().strftime('%Y'))
        date = int(datetime.date.today().strftime('%d'))
        month = int(datetime.date.today().strftime('%m'))
        temp = datetime.date(year, month, date)
        current_date = temp.strftime("%Y%m%d")  # 20220311
        order_number = current_date + str(self.id)
        return order_number

    def update_order_products_with_current_product_price(self):

        for i in self.orderproducts_set.all():
            i.product_price = i.product.price
            i.save()

        from django.db.models import F
        self.orderproducts_set.all().update(product_price=F('product__price'))


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    variations = models.ManyToManyField(Variation, blank=True)

    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name

# Model changes
# Code format
# Add Email Notification
#  - New Order notification
# Celery (Backend Task)
# Celery Beat Scheduler
#   - Daily Email Notification about us
