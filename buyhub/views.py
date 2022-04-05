from django.db.models import Avg
from django.shortcuts import render
from store.models import Product, ReviewRating


def home(request):
    products = Product.objects.all().filter(
        is_available=True).order_by('created_date').annotate(average=Avg('reviewrating__rating'))
    products = list(products)

    context = {
        'products': products,
    }

    return render(request, 'home.html', context)
