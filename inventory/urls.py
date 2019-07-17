from django.urls import path

from .views import index, stock_quantity

app_name = 'inventory'
urlpatterns = [
    path('', index, name='index'),
    path('stock_quantity/', stock_quantity),
]