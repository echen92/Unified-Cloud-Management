from django.contrib.auth.models import User
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    amazon_client_id = models.CharField(max_length=50, blank=True)
    amazon_secret = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, default='M')
    services = models.ManyToManyField(Service, blank=True)

    def __unicode__(self):
        return self.user.email
