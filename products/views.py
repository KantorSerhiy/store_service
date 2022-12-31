from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from products.models import Product, Category, Basket
from users.models import User


def index(request):
    return render(request, "products/index.html")


def products(request, category_id=None):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    context = {
        "title": "Catalog",
        "products": products,
        "category": Category.objects.all(),
    }
    return render(request, "products/products.html", context=context)


@login_required
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


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META["HTTP_REFERER"])
