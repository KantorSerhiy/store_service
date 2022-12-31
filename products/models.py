from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="photo")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Name: {self.name}, price: {self.price}"


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):  # TODO make basket single page
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Basket for {self.user.username}, product {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity
