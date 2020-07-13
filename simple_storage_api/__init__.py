import ast
import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import falcon
from redis import Redis

logger = logging.getLogger(__name__)
logger.addHandler(RotatingFileHandler(f'{os.environ.get("LOG_DIR", "/tmp")}/app.log'))
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
logger.setLevel(logging.INFO)
logger.info("Starting API")

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")


class FalconException(Exception):
    def handle(ex, req, resp, params):
        resp.status = falcon.HTTP_400
        response = json.loads(json.dumps(ast.literal_eval(str(ex))))
        resp.body = json.dumps(response)
        logger.info(resp.body)


def get_redis_client():
    redis_client = Redis(host=REDIS_HOST)
    return redis_client

def validate_redis():
    try:
        c = get_redis_client()
        if c:
            c.set(name="test", value="test")
            c.get("test")
            c.delete("test")
            return True
    except:
        return False

