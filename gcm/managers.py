import requests
import json
import logging


logger = logging.getLogger(__name__)


def send_gcm_notification(api_key, device, message):
    """
    Send gcm message to specific device

    In order to send push message(notification) need to send POST request GCM
    connection server(its provided by google). POST request url should be
    "https://android.googleapis.com/gcm/send". Need to add API_KEY to the
    request header, since GCM using API key authentication

    Args:
        api_key - google API key
        device - gcm device
        message - push message(message need to be send)
        collapse_key - other key
    """
    #
    # values = {
    #   'registration_ids': regs_id,
    #   'data': message,
    #   'time_to_live': 0
    # }
    #
    # time_to_live 0 - messages that can't be delivered immediately will be
    # discarded
    values = {}
    values['registration_ids'] = [device.reg_id]
    values['data'] = message
    values['time_to_live'] = 86400
    data = json.dumps(values)
    logger.debug("send_gcm_notification, request content %s " % (data))

    # header should contain API key and request type
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + api_key,
    }

    response = requests.post(url="https://android.googleapis.com/gcm/send",
                             data=data,
                             headers=headers)
    handle_response(device, response)


def handle_response(device, response):
    """
    Handle GCM response comes from google API

    When the message is processed successfully, the HTTP response has a 200
    status and the body contains more information about the status of the
    message (including possible errors). When the request is rejected, the HTTP
    response contains a non-200 status code (such as 400, 401, or 503).

    More information (http://developer.android.com/google/gcm/http.html)

    Args:
        device: GCM device
        response: server response

    Returns:
        success/ fail status of the GCM notification
    """
    logger.debug("handle_response, status %s, content %s " %
                 (response.status_code, response.content))
    if response.status_code == 200:
        # GCM message processed successfully
        return handle_success_response(device, response.content)
    else:
        # error response
        logger.debug("handle_response, GCM not sent, status code - %s " %
                     (response.status_code))
        return False


def handle_success_response(device, response_content):
    """
    When a JSON request is successful (HTTP status code 200), the response body
    contains a JSON object with the following fields
        1. multicast_id
        2. success
        3. failure
        4. canonical_ids
        5. results
    Several scenarios that need to be considered according to these fields

    Args:
        device: GCM device
        response_content: JSON object
    """
    gcm_response = json.loads(response_content)
    if gcm_response['failure'] == 0 and gcm_response['canonical_ids'] == 0:
        # no need to parser rest of the response
        # message processed successfully
        logger.debug("handle_success_response, successfully sent GCM")
        return True
    elif 'message_id' in gcm_response['results'][0]:
        # need further processing of response
        # check for registration id for replace
        if 'registration_id' in gcm_response['results'][0]:
            # replace the original ID with the new value
            device.reg_id = gcm_response['results'][0]['registration_id']
            device.save()
            logger.debug("handle_success_response, replaced reg_id %s " %
                         (gcm_response['results'][0]['registration_id']))

        return True
    else:
        # error response, extract error
        if gcm_response['results'][0]['error'] == 'NotRegistered':
            # so delete device
            device.delete()
            logger.debug("handle_success_response, deleted device, error %s " %
                         (gcm_response['results'][0]['error']))
        else:
            # ignore error
            logger.debug("handle_success_response, error %s " %
                         (gcm_response['results'][0]['error']))

    return False
