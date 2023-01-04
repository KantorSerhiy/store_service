from django.urls import path
from orders.views import OrderCreateView

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="create")
]

app_name = "orders"
