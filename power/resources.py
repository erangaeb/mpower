from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource
from power.models import Power


class PowerResource(ModelResource):
    class Meta:
        queryset = Power.objects.all()
        resource_name = 'mesuments'
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
