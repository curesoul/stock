from django.shortcuts import render

from .models import Item, In, Out, Position


def index(request):
    obj = Position.objects.all()
    return render(request, 'inventory/index.html', {'objects': obj})


def stock_quantity(request):
    obj = Item.objects.all()
    return render(request, 'inventory/stock_quantity.html', {'objects': obj})
