
from django.urls import path
from items.apps import PaymentsConfig
from items.views import ItemView, BuyView

app_name = PaymentsConfig.name
urlpatterns = [path('item/<int:pk>', ItemView.as_view(), name='item'),
               path('buy/<int:pk>',BuyView.as_view(), name='buy_item'),
               ]