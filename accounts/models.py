import pickle
import base64
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
# from oauth2client.django_orm import FlowField
# from oauth2client.django_orm import CredentialsField
from allauth.socialaccount.models import SocialToken
#
#
# class CredentialsModel(models.Model):
#     id = models.ForeignKey(User, primary_key=True)
#     credential = CredentialsField()
#
#
# class CredentialsAdmin(admin.ModelAdmin):
#     pass
#
# admin.site.register(CredentialsModel, CredentialsAdmin)


class Service(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


# class AmazonCredentials(models.Model):
#     client_id = models.CharField(max_length=50)
#     secret = models.CharField(max_length=50)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # amazon_creds = models.OneToOneField(AmazonCredentials, blank=True, null=True)
    amazon_client_id = models.CharField(max_length=50, blank=True)
    amazon_secret = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, default='M')
    services = models.ManyToManyField(Service, blank=True)

    def __unicode__(self):
        return self.user.email
