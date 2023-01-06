from products.models import Basket


def basket(request):
    user = request.user
    return {
        "basket": Basket.objects.filter(user=user).select_related("product")
        if user.is_authenticated
        else []
    }
