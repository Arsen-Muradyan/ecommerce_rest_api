from .models import SocialNetwork
from rest_framework import serializers

class SocialNetworksSerializer(serializers.ModelSerializer):
  class Meta:
    model = SocialNetwork
    fields = ['title', 'link']
    read_only_fields = ['title', 'link']
