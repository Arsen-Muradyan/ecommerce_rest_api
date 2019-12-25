from django.urls import path, include
from rest_framework import routers
from .api import SocialNetworkViewSet
from . import views
router = routers.DefaultRouter()
router.register('networks', SocialNetworkViewSet)
urlpatterns = [
  path('', include(router.urls))
]
