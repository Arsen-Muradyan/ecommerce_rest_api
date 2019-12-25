from rest_framework import viewsets
from .serializers import SocialNetworksSerializer
from .models import SocialNetwork

class SocialNetworkViewSet(viewsets.ModelViewSet):
  queryset = SocialNetwork.objects.all()
  serializer_class = SocialNetworksSerializer