import ast
import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import falcon

logger = logging.getLogger(__name__)
logger.addHandler(RotatingFileHandler(f'{os.environ.get("LOG_DIR", "/tmp")}/app.log'))
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
logger.setLevel(logging.INFO)
logger.info("Starting API")


class FalconException(Exception):
    def handle(ex, req, resp, params):
        resp.status = falcon.HTTP_400
        response = json.loads(json.dumps(ast.literal_eval(str(ex))))
        resp.body = json.dumps(response)
        logger.info(resp.body)
