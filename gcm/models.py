from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from gcm.managers import send_gcm_notification
import logging


logger = logging.getLogger(__name__)


class Device(models.Model):
    """
    Model class to keep google could messaging enable device details

    Need to keep device registration id as well as active state. There's a
    REST api to deal with these devices. API doing registering and
    un-registering devices

    When registering create a Device with is_active True,
    when un-registering update value of is_active to False
    """
    name = models.CharField(max_length=64, null=True, blank=True)
    device_id = models.CharField(max_length=64, unique=True)
    reg_id = models.TextField()
    user = models.ForeignKey(User)

    def send_message(self, message):
        """
        Send push message to device. Use API key defined in settings since
        gcm use API key authentication
        Actual message sending process delegates to gcm/managers
        'send_gcm_notification' method

        Args:
            message - push message(message need to be send)
        """
        logger.debug("send_message, message %s, user %s, device %s " %
                                    (message, self.user.email, self.device_id))
        send_gcm_notification(api_key=settings.GCM_APIKEY,
                              device=self,
                              message={'msg': message})
