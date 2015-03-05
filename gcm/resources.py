from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource
from gcm.models import Device


class DeviceResource(ModelResource):
    class Meta:
        queryset = Device.objects.all()
        resource_name = 'devices'
        include_resource_uri = False
        allowed_methods = ['get', 'post', 'put']
        authorization = DjangoAuthorization()
        authentication = BasicAuthentication()

    def apply_authorization_limits(self, request, object_list):
        """
        Filter only own devices of request user, some part of authorization
        handles in here as well
        """
        return object_list.filter(user=request.user)
