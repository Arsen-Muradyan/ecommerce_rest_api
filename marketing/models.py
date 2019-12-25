from django.db import models

# Create your models here.
class SocialNetwork(models.Model):
  PROPERTIES = (
    ('Facebook', 'Facebook'),
    ('Twitter', "Twitter"),
    ('Instagram', "Instagram"),
    ('Linkedin', "Linkedin"),
    ('Tumblr', "Tumblr")
  )
  title = models.CharField(max_length=255, choices=PROPERTIES)
  link = models.URLField(max_length=255)
  def __str__(self):
    return self.title
  