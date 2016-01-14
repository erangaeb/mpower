from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource
from gcm.models import Device


class BaseAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        print(request.user)
        print(request)
        #return request.user.is_authenticated()
        return True


class DeviceResource(ModelResource):
    class Meta:
        queryset = Device.objects.all()
        resource_name = 'devices'
        include_resource_uri = False
        allowed_methods = ['get', 'post', 'put']
        #authorization = DjangoAuthorization()
        #authentication = BasicAuthentication()
        authentication = BaseAuthentication()

    def apply_authorization_limits(self, request, object_list):
        """
        Filter only own devices of request user, some part of authorization
        handles in here as well
        """
        print(request.user)
        #return object_list.filter(user=request.user)
        return object_list

    def obj_create(self, bundle, request=None, **kwargs):
        """
        Override this method in order to avoid to do unauthorized things, get
        user from request and set it as device user
        """
        # set modified date to none since no update yet
        #logger.debug("obj_create: %s " % (bundle.data))
        return super(DeviceResource, self).obj_create(bundle, request,
                                                      user=request.user)

    '''
    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del(data_dict['meta'])
        return data_dict
    '''
