from django.shortcuts import render
from django.views import generic

from orders.forms import OrderForm


class OrderCreateView(generic.CreateView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
