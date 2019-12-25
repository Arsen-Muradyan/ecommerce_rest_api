from rest_framework import viewsets, permissions, generics
from .serializers import CartItemSerializer, CartSerializer
from .models import Cart, CartItem
from products.models import Product
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
class CartAPI(viewsets.ViewSet):
  serializer_class = CartSerializer
  permission_classes = [
    permissions.IsAuthenticated
  ]
  # All User Carts
  def list(self, request):
    queryset = Cart.objects.filter(user=self.request.user)
    serializer = CartSerializer(queryset, many=True)
    return Response({
      "carts": serializer.data
    })
  # Show One Cart with Order Data
  def retrieve(self, request, pk=None):
    queryset = Cart.objects.filter(user=self.request.user)
    cart = get_object_or_404(queryset, pk=pk)
    orders = CartItem.objects.filter(cart=cart)
    return Response({
      "cart": CartSerializer(instance=cart).data,
      "orderResponses": CartItemSerializer(orders, many=True).data
    })
  # Calculate Product Price
  def calculate(self, product):
    price = product.price
    if product.discount > 0:
      price = product.discount
    return price
  # Create Order return Function
  def create_order(self, product, cart, quantity):
    serializer = CartItemSerializer(data={
      "product": product,
      "cart": cart,
      "quantity": quantity
    })
    serializer.is_valid(raise_exception=True)
    cart_item = serializer.save()
    return CartItemSerializer(cart_item).data
  # Create Cart and add products to cart
  def create(self, request):
    if request.data.get('product_id') and request.data.get('quantity'):
      # Get Product
      try:
        product = Product.objects.get(
          id=request.data['product_id'])
      except ObjectDoesNotExist:
        return Response({
          "status": 404,
          "message": "Product Does Not Exisits"
        })
      # Check Cart on Session
      if 'cart' in  request.session:
        cart = Cart.objects.get(id=request.session['cart'])
        cart_exists = CartItem.objects.filter(
          product=product,
          cart=cart
        ).first()
        # Check if product alread added to cart
        if cart_exists:
          price = self.calculate(product)
          cart.total += Decimal(request.data['quantity'] * price)
          cart_exists.quantity += request.data['quantity']
          cart_exists.save()
          cart.save()
          return Response({
            "order": CartItemSerializer(cart_exists).data
          })
        else:
          # if product not added cart
          cart_item = self.create_order(
            self.request.data.get('product_id'),
            self.request.session['cart'],
            self.request.data.get('quantity')
          )
          price = self.calculate(product)
          cart.total += Decimal(request.data['quantity'] * price)
          cart.save()
          return Response({
            "order": cart_item
          })
      else: 
        # Create Cart And add product to card
        price = self.calculate(product)
        serializer = CartSerializer(data={
          "user": self.request.user.id,
          "total": request.data.get('quantity') * price
        })
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()
        request.session['cart'] = CartSerializer(cart).data['id']
        request.session.save()
        cart_item = self.create_order(
          self.request.data.get('product_id'),
          self.request.session['cart'],
          self.request.data.get('quantity')
        )
        return Response({
          "cart": CartSerializer(cart).data,
          "order": cart_item
        })
    return Response({
      "status": 401,
      "message": "Product not added "
    })
  # Delete Cart 
  def destroy(self, request, pk=None):
    queryset = Cart.objects.filter(user=self.request.user)
    cart = get_object_or_404(queryset, pk=pk)
    cart.delete()
    serializer = CartSerializer(cart)
    if 'cart' in request.session:
      del request.session['cart']
    return Response({
      "cart": serializer.data
    })
class OrdersAPI(viewsets.ViewSet):
  permission_classes = [
    permissions.IsAuthenticated
  ]
  # Update Order From Cart
  def partial_update(self, request, pk=None):
    if 'cart' in request.session:
      instance = CartItem.objects.filter(
        id=pk, cart=request.session['cart']).first()
      serializer = CartItemSerializer(instance, {
        "quantity": request.data.get('quantity')
      }, partial=True)
      serializer.is_valid(raise_exception=True)
      order = serializer.save()
      return Response({
        "order": CartItemSerializer(order).data
      })
      