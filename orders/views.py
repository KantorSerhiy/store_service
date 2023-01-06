import stripe

from http import HTTPStatus
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class SuccessTemplateView(TitleMixin, generic.TemplateView):
    template_name = "orders/success.html"
    title = "Store - tnx for order!"


class CancelTemplateView(TitleMixin, generic.TemplateView):
    template_name = "orders/cancel.html"
    title = "Something wrong =("


class OrderListView(TitleMixin, generic.ListView):
    template_name = "orders/orders.html"
    title = "Store - Orders"
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(generic.DetailView):
    template_name = "orders/order.html"
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context["title"] = f"Store - Order #{self.object.id}"
        return context


class OrderCreateView(TitleMixin, generic.CreateView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:create")
    title = "Store - Create Order"

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={"order_id": self.object.id},
            mode="payment",
            success_url=f"{settings.DOMAIN_NAME}{reverse('orders:order-success')}",
            cancel_url=f"{settings.DOMAIN_NAME}{reverse('orders:order-canceled')}",
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
