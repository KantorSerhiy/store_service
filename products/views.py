from django.shortcuts import render
from products.models import Product, Category


def index(request):
    return render(request, "products/index.html")


def products(request):
    context = {
        "title": "Catalog",
        "products": Product.objects.all(),
        "category": Category.objects.all(),
    }
    return render(request, "products/products.html", context=context)
