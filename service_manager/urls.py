from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^connect_amazon', views.connect_amazon, name='connect_amazon'),
                       url(r'^amazon/files$', views.amazon_file_view, name='amazon_file_view'),
                       url(r'^dropbox/files$', views.dropbox_file_view, name='dropbox_file_view'),
                       url(r'^dropbox/auth_start$', views.dropbox_auth_start, name='dropbox_auth_start'),
                       url(r'^dropbox/auth_finish$', views.dropbox_auth_finish, name='dropbox_auth_finish'),
                       url(r'^google/files$', views.google_file_view, name='google_file_view'),
                       )
