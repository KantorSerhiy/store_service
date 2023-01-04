from django.urls import reverse_lazy
from django.views import generic

from common.views import TitleMixin
from orders.forms import OrderForm


class OrderCreateView(TitleMixin, generic.CreateView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:create")
    title = "Store - Create Order"

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
