import os

from common.dao.user_store import UserStore
from common.dao.trace_store import TraceStore
from api.trace import handle_trace

USERSTORE_TABLENAME = os.getenv("USERSTORE_TABLENAME")
TRACESTORE_TABLENAME = os.getenv("TRACESTORE_TABLENAME")
userStore = UserStore(USERSTORE_TABLENAME)
traceStore = TraceStore(TRACESTORE_TABLENAME)


def handler(event, context):
    api_handler = {
        '/trace': lambda: handle_trace(event, traceStore, userStore),
    }

    if 'resource' in event:
        return api_handler[event['resource']]()

    return {
        'statusCode': 500,
        'body': 'Internal Server Error'
    }
