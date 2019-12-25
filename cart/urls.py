from django.urls import path, include
from .api import CartAPI, OrdersAPI

urlpatterns = [
  path('cart/', CartAPI.as_view({'get': 'list'})),
  path('cart/<int:pk>', CartAPI.as_view({'get': 'retrieve'})),
  path('cart/add', CartAPI.as_view({'post': 'create'})),
  path('cart/<int:pk>/delete', CartAPI.as_view({'delete': 'destroy'})),
  path('orders/<int:pk>/update', OrdersAPI.as_view({"put": "partial_update"}))

]