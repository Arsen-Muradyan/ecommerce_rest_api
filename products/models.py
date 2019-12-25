from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils import timezone
# Create your models here.
class Product(models.Model):
  title = models.CharField(max_length=255)
  image = models.ImageField(upload_to="images/")
  price = models.FloatField()
  PRIORITIES = (
    (1, 'Very Low'),
    (2, 'Low'),
    (3, 'Normal'),
    (4, "Great"),
    (5, "Perfect")
  )
  rating = models.IntegerField(choices=PRIORITIES)
  discount = models.FloatField()
  def __str__(self):
    return self.title
