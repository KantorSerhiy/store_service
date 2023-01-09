from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):
    CREATED, PAID = 0, 1
    STATUSES = (
        (CREATED, "Created"),
        (PAID, "Paid"),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id}.{self.first_name} {self.last_name}"

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            "purchased_items": [basket.de_json() for basket in baskets],
            "total_sum": float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
