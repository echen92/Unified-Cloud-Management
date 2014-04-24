from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^amazon/files$', views.amazon_file_view, name='amazon_file_view'),
                       url(r'^dropbox/files$', views.dropbox_file_view, name='dropbox_file_view'),
                       url(r'^dropbox/upgrade_token', views.dropbox_upgrade_token, name='dropbox_upgrade_token'),
                       url(r'^google/files$', views.google_file_view, name='google_file_view'),
)
