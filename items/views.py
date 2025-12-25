
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
import stripe

from config.settings import USD_KEY, EUR_KEY
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

        for order_item in order.items:
            print('запрос')
            if order_item.item.currency=='USD':
                stripe.api_key = USD_KEY
            else:
                stripe.api_key = EUR_KEY

            product = stripe.Product.create(
                name=order_item.item.name,
                default_price_data={"unit_amount": int(order_item.item.price), "currency": order_item.item.currency},
                expand=["default_price"],
            )
            prices.append({'price': product.default_price.id, 'quantity': order_item.quantity})

        session = stripe.checkout.Session.create(
            success_url="http://localhost:8000/success_page.html",
            line_items=prices,
            mode="payment",
        )

        return JsonResponse({'session': session})

class CartView(View):
    template_name = 'cart.html'

    def get(self, request,  pk=None):
        order_pk = self.request.session['order_id']
        order = get_object_or_404(Order, pk=order_pk)
        return render(request, 'cart.html', {'order': order,'items': order.items})

class OrderView(View):
    model = Order
    template_name = 'cart.html'

    def get(self, request, pk):
        return redirect('/items/cart')

    def post(self, request, pk):
        if self.request.session.get('order_id'):
            return JsonResponse({'order_id': None})
        item = get_object_or_404(Item, pk=pk)
        order = Order.objects.create(user=request.user)
        OrderItem.objects.create(item=item, quantity=1, order=order)
        self.request.session['order_id'] = order.pk
        return JsonResponse({'order_id': order.pk})

    def put(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        order_id = request.session.get('order_id')
        order = Order.objects.get(pk=order_id)
        order_item , created  = OrderItem.objects.get_or_create(order = order, item=item)
        order_item.quantity = order_item.quantity + 1
        order_item.save()
        order_pk = self.request.session['order_id']
        return JsonResponse({'order_id': order_pk})


