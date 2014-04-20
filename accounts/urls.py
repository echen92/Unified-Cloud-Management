from django.conf.urls import patterns, url
import accounts.views

urlpatterns = patterns('',
                       url(r'^login', accounts.views.login, name='login'),
                       url(r'^signup', accounts.views.email_signup, name='email_signup'),
                       url(r'^logout', accounts.views.logout, name='logout'),
                       url(r'^connect_amazon', accounts.views.connect_amazon, name='connect_amazon'),
                       )
