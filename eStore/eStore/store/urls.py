from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:pk>/', views.product, name='product details')
]

