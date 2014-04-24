from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^amazon/files$', views.amazon_file_view, name='amazon-file-view'),
                       url(r'^dropbox/files$', views.dropbox_file_view, name='dropbox-file-view'),
                       url(r'^google/files$', views.google_file_view, name='google-file-view'),
)
