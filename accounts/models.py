import pickle
import base64
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()


class CredentialsAdmin(admin.ModelAdmin):
    pass

admin.site.register(CredentialsModel, CredentialsAdmin)


#  Actual models start below, above = auth stuff
class Service(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, default='M')
    services = models.ManyToManyField(Service, blank=True)

    def __unicode__(self):
        return self.user.email
