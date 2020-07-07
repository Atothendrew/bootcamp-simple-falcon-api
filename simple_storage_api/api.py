__author__ = 'Andrew Williamson <axwilliamson@godaddy.com>'

import json

import falcon

from simple_storage_api import FalconException, get_redis_client
from simple_storage_api.middleware import RequestIDMiddleware


def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPPayloadTooLarge(
                'Request body is too large', msg)

    return hook


class RootURI:
    DEFAULT_BODY = "Hello World! You did it!"

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.body = RootURI.DEFAULT_BODY
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT


class ExampleDataStore():
    REDIS_KEY = "db_store"

    def on_get(self, req, resp):
        """Handles GET requests"""
        redis_client = get_redis_client()
        value = redis_client.get(self.REDIS_KEY)
        if not value:
            resp.status = falcon.HTTP_404
            resp.media = {"error": "Could not find data in redis"}
        else:
            resp.media = json.loads(value.decode('utf-8'))
            resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        try:
            body = req.media
        except AttributeError:
            raise falcon.HTTPBadRequest("Body must be valid json")

        redis_client = get_redis_client()
        current_val = redis_client.get(self.REDIS_KEY)
        if current_val:
            value = json.loads(current_val.decode('utf-8'))
            value.update(**body)
        else:
            value = body

        redis_client.set(self.REDIS_KEY, json.dumps(value))
        redis_client.save()

        resp.body = json.dumps(body)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_201


api = falcon.API(middleware=[RequestIDMiddleware()])
api.add_route('/', RootURI())
api.add_route('/db', ExampleDataStore())
api.add_error_handler(FalconException)
