from django.test import TestCase
from django.test import Client
from datetime import datetime
from django.utils.timezone import utc
import json

from gcm.models import Device
from django.contrib.auth.models import User


def get_dummy_user(username, password, email='test@test.com'):
    """
    Create dummy user objects, need user objects to test function in all apps
    need to set users password in here in order to login

    Args:
        username: users username
        password: users password

    Return:
        user: user object
    """
    user = User.objects.create_user(username=username,
                                    password='test',
                                    email=email)
    user.set_password(password)
    user.is_active = True
    user.is_superuser = True
    user.save()

    return user


class DeviceAPITests(TestCase):

    def setUp(self):
        """
        Create client here, client need to handle all the function with API,
        we use client to test 'GET', 'POST', 'PUT', 'PATCH', 'DELETE' function
        of device api

        This client is not a authenticated client, so need to login with this
        client when testing above functions
        """
        self.client = Client()

    def get_dummy_device(self, user, reg_id='dummyregid', dev_id='dummydevid'):
        """
        Create dummy object, in devices api directly deal with device models,
        so we dummy device objects

        Args:
            user: objects owner
            reg_id: registration id

        Return:
            device: object
        """
        device = Device.objects.create(name='dummy_device',
                            device_id=dev_id,
                            reg_id=reg_id,
                            created_date=datetime.utcnow().replace(tzinfo=utc),
                            user=user)

        return device

    def get_dummy_json_device(self, reg_id, dev_id, ):
        """
        Create dummy JSON object with device details, this json object can be
        use to test POST function with device API

        Args:
            reg_id: device registration id

        Returns:
            json string
        """
        json_device = \
            """
            {
                "name": "dummy_device",
                "device_id": "%s",
                "reg_id": "%s"
            }
            """ \
            % (dev_id, reg_id)

        return json_device

    def test_create_device_with_unauthenticated_user(self):
        """
        API only allow to create devices only for authenticated users, do when
        user is un authenticated api should raises HTTP 401
        """
        # create dummy objects and url
        get_dummy_user('test', '123')
        api_url = "/api/v1/devices/"

        # send POST request with unauthenticated users
        # api should return 401
        response = self.client.post(api_url, "neverMindTheDataAtThisPoint",
                                    content_type="application/json")
        self.failUnlessEqual(response.status_code, 401)

    def test_create_device_with_authenticated_user(self):
        """
        Api allow to create devices to authenticated users, so in here API
        should return HTTP 201(created)
        """
        # create dummy objects and url
        user = get_dummy_user('test', '123')
        json_device = self.get_dummy_json_device('dummyregid', 'devid')
        api_url = "/api/v1/devices/"

        # login with client(so request is authenticated)
        # send POST request, status should be 201
        self.client.login(username='test', password='123')
        response = self.client.post(api_url, json_device,
                                    content_type="application/json")
        self.failUnlessEqual(response.status_code, 201)

        # device should be created
        devices = Device.objects.filter(user=user)
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0].reg_id, 'dummyregid')
        self.assertEqual(devices[0].device_id, 'devid')
