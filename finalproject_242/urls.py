from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finalproject_242.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^social_accounts/', include('allauth.urls')),
    url(r'^accounts/', include('accounts.urls')),
    # url(r'dashboard/', 'accounts.views.dashboard', name='dashboard'),
    url(r'^', include('website.urls')),
)
