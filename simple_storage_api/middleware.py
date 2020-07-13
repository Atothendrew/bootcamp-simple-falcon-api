__author__ = 'Andrew Williamson <axwilliamson@godaddy.com>'

from uuid import uuid4

from simple_storage_api import logger
from simple_storage_api.context import ctx


class RequestIDMiddleware:
    def process_request(self, req, resp):
        ctx.request_id = str(uuid4())
        logger.info(f'Start {ctx.request_id} - {req.method} {req.relative_uri} {req.content_type}')

    def process_response(self, req, resp, resource, req_succeeded):
        logger.info(f'End {ctx.request_id}')
