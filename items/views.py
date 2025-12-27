from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView, FormView
import stripe

from config.settings import USD_KEY, EUR_KEY, stripe_public
from items.models import Item, Order, OrderItem
from items.utils import check_discounts_and_tax


# Create your views here.

class ItemView(DetailView):
    model = Item
    template_name = 'item.html'


class ItemsView(ListView):
    model = Item
    template_name = 'items.html'


class ChangeCurrency(FormView):

    def post(self, request, *args, **kwargs):
        print('here')
        order_pk = self.request.session.get('order_id')
        order = get_object_or_404(Order.objects.prefetch_related('order_items'), pk=order_pk)
        order_products = order.order_items.all()
        currency = request.POST.get('currency')


        if currency == 'USD':
            stripe.api_key = USD_KEY
        elif currency == 'EUR':
            stripe.api_key = EUR_KEY

        order_products.update(currency=currency)

        return redirect('items:cart')


class BuyView(View):
    template_name = 'success_page.html'
    model = Order

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        prices = []

        coupon_obj, tax_rate_id = check_discounts_and_tax(order)
        try:
            for order_item in order.items:
                product = stripe.Product.create(
                    name=order_item.item.name,
                    default_price_data={"unit_amount": int(order_item.item.price),
                                        "currency": order_item.currency},
                    expand=["default_price"],

                )
                prices.append(
                    {'price': product.default_price.id, 'quantity': order_item.quantity, 'tax_rates': tax_rate_id})

            session = stripe.checkout.Session.create(
                success_url="http://localhost:8000/success_page.html",
                line_items=prices,
                mode="payment",
                discounts=coupon_obj,

            )
        except stripe.StripeError as e:
            print("Ошибка в страйп", e)
            return JsonResponse({'error': "Ошибка в страйп"}, status=400)

        return JsonResponse({'session': session})


class CartView(View):
    template_name = 'cart.html'

    def get(self, request, pk=None):
        order_pk = self.request.session['order_id']
        order = get_object_or_404(Order, pk=order_pk)
        return render(request, 'cart.html', {'order': order, 'items': order.items, 'stripe_public_key': stripe_public})

    def delete(self, request, pk=None):
        order_pk = self.request.session['order_id']
        order = get_object_or_404(Order.objects.prefetch_related('order_items'), pk=order_pk)
        order_products = order.order_items.all()
        for order_product in order_products:
            order_product.delete()

        return HttpResponse(status=200)


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
        order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
        order_item.quantity = order_item.quantity + 1
        order_item.save()
        order_pk = self.request.session['order_id']
        return JsonResponse({'order_id': order_pk})
