from accounts.models import Account
from category.models import Category
from django.conf import settings
from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse

from .managers import VariationManager

# from django.contrib.auth import get_user_model
# User = get_user_model()


# Create your models here.


class Product(models.Model):
    # ForeignKey fields
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    # ...

    # Normal Fields
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.FloatField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    # Helpers
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def averageReview(self):
        # reviews = self.reviewrating_set.filter(status=True).aggregate(average=Avg('rating'))
        # reviews = self.review_ratings.filter(status=True).aggregate(average=Avg('rating'))
        '''
            review_avg = self.review_ratings.filter(status=True).aggregate(average=Avg('rating'))['average']
            return round(review_avg, 1)
        '''

        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))

        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class Variation(models.Model):
    variation_category_choice = (
        ('color', 'Color'),
        ('size', 'Size'),
    )

    class VARIATION_CATEGORY_CHOICES(models.TextChoices):
        COLOR = 'COLORing', 'Color'
        SIZE = 'SIZE', 'Size'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=VARIATION_CATEGORY_CHOICES.choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

# product = Product.objects.get(id=1)
# product.reviewrating_set.all()


class ReviewRating(models.Model):

    # ForeignKey fields
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='review_ratings')
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='review_ratings')

    # Normal Fields
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)

    # Helpers
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'


class UserGallery(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE)
    # User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'usergallery'
        verbose_name_plural = 'user gallery'
