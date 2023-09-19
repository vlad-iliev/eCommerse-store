from django.shortcuts import render
from .models import *


def index(request):
    context = {

    }

    return render(request, 'common/index.html', context)


def store(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }

    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, }

    context = {
        'items': items,
        'order': order
    }

    return render(request, 'cart/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, }

    context = {
        'items': items,
        'order': order
    }

    return render(request, 'checkout/checkout.html', context)


def product(request, pk):
    product = Product.objects.get(pk=pk)

    context = {
        'product': product,

    }
    return render(request, 'store/product.html', context)
