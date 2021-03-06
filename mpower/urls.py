from django.conf.urls import patterns, include, url
from power.resources import PowerResource
from gcm.resources import DeviceResource
from tastypie.api import Api


v1_api = Api(api_name='v1')
v1_api.register(PowerResource())
v1_api.register(DeviceResource())

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpower.views.home', name='home'),
    # url(r'^mpower/', include('mpower.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # API urls
    (r'^api/', include(v1_api.urls)),
)
