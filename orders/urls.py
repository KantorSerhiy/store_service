from django.urls import path
from orders.views import (
    OrderCreateView,
    SuccessTemplateView,
    CancelTemplateView,
    OrderListView,
    OrderDetailView,
)

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="create"),
    path("order-success/", SuccessTemplateView.as_view(), name="order-success"),
    path("order-canceled/", CancelTemplateView.as_view(), name="order-canceled"),
    path("", OrderListView.as_view(), name="orders"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]

app_name = "orders"
