import io

import wrapt
from hoss_agent import get_logger
from hoss_agent.base import Client
from hoss_agent.conf.constants import EVENT
from uuid import uuid4

import threading

logger = get_logger("hoss_agent")
GLOBAL_CLIENT = None


_lock = threading.Lock()


def init(config=None, *args, **inline):
    global GLOBAL_CLIENT
    if GLOBAL_CLIENT is not None:
        logger.info('Agent already initialized. Exiting')
        return

    with _lock:
        if isinstance(config, str):
            if len(config) == 0 or config == 'None':
                logger.info('Hoss API Key is not provided. Exiting')
                return
            if len(args) >= 1 and isinstance(args[0], dict):
                args[0]['API_KEY'] = config
                client = Client(args[0], **inline)
            else:
                client = Client({"API_KEY": config}, **inline)
        else:
            if not config or 'API_KEY' not in config or config['API_KEY'] == 'None':
                logger.info('Hoss API Key is not provided. Exiting')
                return
            client = Client(config, **inline)

        GLOBAL_CLIENT = client
        client.start_threads()

        # monkey patch write & finish of request handler
        wrapt.wrap_function_wrapper(
            'tornado.web',
            "RequestHandler.write", patched_write,
        )
        wrapt.wrap_function_wrapper(
            'tornado.web',
            "RequestHandler.finish", patched_finish,
        )


def patched_write(wrapped, instance, args, kwargs):
    """
    Patched RequestHandler write method to capture response body
    :param wrapped:
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    _concatenate_response_body(instance, args)
    return wrapped(*args, **kwargs)


def patched_finish(wrapped, instance, args, kwargs):
    """
    Patched RequestHandler finish method to queue event
    :param wrapped:
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    global GLOBAL_CLIENT
    _concatenate_response_body(instance, args)

    if GLOBAL_CLIENT is not None:
        client = GLOBAL_CLIENT

        if GLOBAL_CLIENT.config.should_skip_fn is None or not GLOBAL_CLIENT.config.should_skip_fn(instance):
            client.queue(EVENT, _get_event(instance))

        if hasattr(instance, '_hoss_response'):
            del instance._hoss_response

    return wrapped(*args, **kwargs)


def _concatenate_response_body(request_handler, args):
    if not hasattr(request_handler, '_hoss_response'):
        request_handler._hoss_response = io.BytesIO()
    if len(args) > 0:
        request_handler._hoss_response.write(args[0])


def _get_event(request_handler):
    global GLOBAL_CLIENT
    request_start_time = int(round(request_handler.request._start_time * 1000))
    request_time_ms = int(round(request_handler.request.request_time() * 1000))

    metadata = {}

    if GLOBAL_CLIENT.config.user_data_fn is not None:
        metadata["userData"] = GLOBAL_CLIENT.config.user_data_fn(request_handler)

    data = {
        "eventId": uuid4(),
        "request": {
            "method": request_handler.request.method,
            "headers": dict(request_handler.request.headers),
            "body": request_handler.request.body,
            "url": "%s://%s%s" % (
                request_handler.request.protocol,
                request_handler.request.host,
                request_handler.request.uri
            ),
            "receivedAt": request_start_time
        },
        "response": {
            "headers": dict(request_handler._headers.get_all()),
            "statusCode": request_handler._status_code,
            "receivedAt": request_start_time + request_time_ms,
            "body": request_handler._hoss_response if hasattr(request_handler, '_hoss_response') else None
        },
        "metadata": metadata
    }
    return data


