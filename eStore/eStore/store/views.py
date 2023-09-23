from django.shortcuts import render
from .models import *
from .utils import *
from django.http import JsonResponse
import json
import datetime


def index(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'common/index.html', context)


def store(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cart_items': cart_items,
    }

    return render(request, 'store/store.html', context)


def cart(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }

    return render(request, 'cart/cart.html', context)


def checkout(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }

    return render(request, 'checkout/checkout.html', context)


def product(request, pk):
    product = Product.objects.get(pk=pk)
    data = cart_data(request)
    cart_items = data['cart_items']

    context = {
        'product': product,
        'cart_items': cart_items,

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
    elif action == 'set-to-zero':
        order_item.quantity = 0

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('item was added', safe=False)


def process_order(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        country=data['shipping']['country'],
        city=data['shipping']['city'],
        region=data['shipping']['region'],
        postcode=data['shipping']['postcode'],
    )

    return JsonResponse('Payment compleate', safe=False)
