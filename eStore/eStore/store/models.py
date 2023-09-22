from django.core import validators
from django.db import models
from django.contrib.auth.models import User


# TODO: Fix null&blank fields
# TODO: validatrs
class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    first_name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    surname = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    email = models.EmailField(
        unique=True,
        max_length=200,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.first_name + self.surname


class Product(models.Model):
    title = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    description = models.TextField(
        max_length=800,
        null=True,
        blank=True,
    )

    price = models.FloatField(
    )

    image = models.ImageField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_ordered = models.DateTimeField(
        auto_now_add=True,
    )
    complete = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    transaction_id = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    quantity = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    country = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    city = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    region = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    postcode = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.address
