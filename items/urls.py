
from django.urls import path
from items.apps import PaymentsConfig
from items.views import ItemView, BuyView

app_name = PaymentsConfig.name
urlpatterns = [path('item/<int:pk>', ItemView.as_view(), name='item'),
               path('buy/',BuyView.as_view(), name='buy'),
               ]