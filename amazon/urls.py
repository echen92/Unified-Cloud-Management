from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^files', views.file_view, name='amazon-file-view'),
)
