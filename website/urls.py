from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='website_index'),
                       url(r'^dashboard', views.dashboard, name='dashboard'),
)
