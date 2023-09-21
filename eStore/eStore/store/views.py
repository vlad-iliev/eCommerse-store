from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


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


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', product_id)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('item was added', safe=False)
