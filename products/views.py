from django.shortcuts import render, redirect
from products.models import Product, Category, Basket
from users.models import User


def index(request):
    return render(request, "products/index.html")


def products(request):
    context = {
        "title": "Catalog",
        "products": Product.objects.all(),
        "category": Category.objects.all(),
    }
    return render(request, "products/products.html", context=context)


def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        baskets = baskets.first()
        baskets.quantity += 1
        baskets.save()

    return redirect(request.META["HTTP_REFERER"])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META["HTTP_REFERER"])