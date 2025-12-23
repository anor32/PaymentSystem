from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
import stripe
from items.models import Item, Order, OrderItem


# Create your views here.

class ItemView(DetailView):
    model = Item
    template_name = 'item.html'


class ItemsView(ListView):
    model = Item
    template_name = 'items.html'


class BuyView(View):
    model = Order
    template_name = 'success_page.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        prices = []

        for item in order.items.all():
            product = stripe.Product.create(
                name=item.name,
                default_price_data={"unit_amount": int(item.price), "currency": "usd"},
                expand=["default_price"],
            )

            prices.append({'price': product.default_price.id, 'quantity': product.quantity})

        session = stripe.checkout.Session.create(
            success_url="http://localhost:8000/success_page.html",
            line_items=prices,
            mode="payment",
        )

        return JsonResponse({'session': session})


class OrderView(View):
    model = Order
    template_name = 'cart.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        items = order.items.all().prefetch_related()

        return render(request, 'cart.html', {'order': order, 'items': items})

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        order = Order.objects.create(user=request.user)
        OrderItem.objects.create(item=item, quantity=1, order=order)
        self.request.session['order_id'] = order.pk
        return JsonResponse({'order_id': order.pk})

    def update(self, request, pk):
        item = get_object_or_404(Order, pk=pk)
        order_item = get_object_or_404(OrderItem, item=item)
        order_item.quantity = order_item.quantity + 1
        order_pk = self.request.session['order_id']
        return JsonResponse({'order_id': order_pk})
