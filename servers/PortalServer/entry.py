import os

from common.dao.image_store import ImageStore
from common.dao.user_store import UserStore
from common.dao.trace_store import TraceStore

from api.trace import handle_trace
from api.images import handle_images

USERSTORE_TABLENAME = os.getenv("USERSTORE_TABLENAME")
TRACESTORE_TABLENAME = os.getenv("TRACESTORE_TABLENAME")
S3_BUCKET = os.getenv("S3_BUCKET")
imageStore = ImageStore(S3_BUCKET)
userStore = UserStore(USERSTORE_TABLENAME)
traceStore = TraceStore(TRACESTORE_TABLENAME)


def handler(event, context):
    api_handler = {
        '/trace': lambda: handle_trace(event, traceStore, userStore),
        '/images': lambda: handle_images(event, imageStore, traceStore)
    }

    if 'resource' in event:
        return api_handler[event['resource']]()

    return {
        'statusCode': 500,
        'body': 'Internal Server Error'
    }
