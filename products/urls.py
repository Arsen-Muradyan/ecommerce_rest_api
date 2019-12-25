from django.urls import path, include
from rest_framework import routers
from .api import ProductViewSet
from . import views
router = routers.DefaultRouter()
router.register('products', ProductViewSet)
urlpatterns = [
    path('', include(router.urls))
]
