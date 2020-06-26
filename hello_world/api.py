__author__ = 'Andrew Williamson <axwilliamson@godaddy.com>'

import json

import falcon

from hello_world import FalconException
from hello_world.middleware import RequestIDMiddleware


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

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.media = "Hello World! You did it!"
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        try:
            body = req.media
        except AttributeError:
            raise falcon.HTTPBadRequest("Body must be valid json")

        resp.body = json.dumps(body)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_201


api = falcon.API(middleware=[RequestIDMiddleware()])
api.add_route('/', RootURI())
api.add_route('/db', ExampleDataStore())
api.add_error_handler(FalconException)
