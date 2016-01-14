from django.conf.urls.defaults import *
from django.core import serializers
from django.http import HttpResponse
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from power.models import Power
from gcm.models import Device

import logging
import json


logger = logging.getLogger(__name__)


class PowerResource(ModelResource):
    class Meta:
        queryset = Power.objects.all()
        resource_name = 'mesuments'
        include_resource_uri = False
        allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        authentication = BasicAuthentication()

    def override_urls(self):
        """
        Add invoice history retrieving url here

        We don't use any resource to deal with invoice histories, instead
        add url entry that maps to 'invoices/<invoice_id>/history'. When
        request comes to this url 'get_history' method will be call
        """
        return [
            url(r"^(?P<resource_name>%s)/latest%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_latest'),
                name="api_get_history"
            ),
        ]

    def get_latest(self, request, **kwargs):
        """
        When request comes with 'mesuments/<id>/latest' url this method
        will be invoke, need to extract latest mesument entry and return it.

        The response will be return as a JSON object
        """
        # need to check the
        #   1. request type
        #   2. user authentication
        self.method_check(request, allowed=['get'])
        obj = Power.objects.all().order_by('-id')[0]
        data = serializers.serialize('json', [obj, ])
        struct = json.loads(data)
        data = json.dumps(struct[0])

        resp_dict = {}
        resp_dict['voltage'] = str(obj.voltage)
        resp_dict['current'] = str(obj.current)
        resp_dict['frequency'] = str(obj.frequency)
        resp_dict['kwh'] = str(obj.kwh)

        response = HttpResponse(json.dumps(resp_dict),
                                           mimetype='application/json')
        response['Access-Control-Allow-Origin'] = '*'

        return response

    def apply_authorization_limits(self, request, object_list):
        """
        Filter only own devices of request user, some part of authorization
        handles in here as well
        """
        user = User.objects.get(id=1)
        return object_list.filter(user=user)

    def obj_create(self, bundle, request=None, **kwargs):
        """
        Override this method in order to avoid to do unauthorized things, get
        user from request and set it as power user
        """
        # set modified date to none since no update yet
        #logger.debug("obj_create: %s " % (bundle.data))
        notify_over_usage(bundle)
        user = User.objects.get(id=1)
        print(user)
        return super(PowerResource, self).obj_create(bundle, request,
                                                     user=user)


def notify_over_usage(bundle):
    """
    Detect over usage according to the voltage
    For demo purpose, voltage higher than 253 cosider as over usage
    """
    voltage = bundle.data['voltage']
    logger.debug("voltage %s " % (voltage))

    if voltage > 253:
        # over usage, notify via GCM
        device = Device.objects.get(id=1)
        print(device.reg_id)
        device.send_message('OVER')
