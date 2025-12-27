
from django.urls import path
from items.apps import PaymentsConfig
from items.views import ItemView, BuyView, ItemsView, OrderView, CartView, ChangeCurrency

app_name = PaymentsConfig.name
urlpatterns = [path('item/<int:pk>', ItemView.as_view(), name='item'),
               path('buy/<int:pk>',BuyView.as_view(), name='buy_item'),
                path('',ItemsView.as_view(), name='all_items'),
                path('order/<int:pk>',OrderView.as_view(), name='order_create'),
               path('cart/',CartView.as_view(), name='cart'),
               path('change/curency/', ChangeCurrency.as_view(), name='change_currency'),
               ]