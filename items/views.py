from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import CreateView, DetailView
import stripe
from items.models import Item


# Create your views here.

class ItemView(DetailView):
    model = Item
    template_name = 'items.html'





class BuyView(View):
    model = Item
    template_name = 'success_page.html'


    def get(self,request,pk):
        item = get_object_or_404(Item, pk=pk)
        product = stripe.Product.create(
            name=item.name,
            default_price_data={"unit_amount": int(item.price), "currency": "usd"},
            expand=["default_price"],
        )

        price = product.default_price.id
        session = stripe.checkout.Session.create(
            success_url="http://localhost:8000/success_page.html",
            line_items=[{"price": price, "quantity": 1}],
            mode="payment",
        )

        return JsonResponse({'session': session})
