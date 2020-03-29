import re
import os
from common.dao.image_store import ImageStore
from common.dao.user_store import UserStore
from common.dao.trace_store import TraceStore

S3_BUCKET = os.getenv("S3_BUCKET")
USERSTORE_TABLENAME = os.getenv("USERSTORE_TABLENAME")
TRACESTORE_TABLENAME = os.getenv("TRACESTORE_TABLENAME")
userStore = UserStore(USERSTORE_TABLENAME)
traceStore = TraceStore(TRACESTORE_TABLENAME)


def validate(event):
    fields_available = 'id' in event and 'image' in event
    id_valid = None
    if fields_available:
        id_valid = re.match("[0-9a-f]{32}", event['id'])
    return fields_available and id_valid


def handler(event, context):
    if not validate(event):
        return {
            'statusCode': 400,
            'body': 'Malformed/Invalid request'
        }

    # Extract components we need from the event
    identifier = event['id']
    image = event['image']
    deviceID = event['deviceID']

    # Upload the base64 image as a JPG
    imageStore = ImageStore(S3_BUCKET)
    imageStore.append(identifier, image)

    # Update both the user stores and trace stores about the new person
    traceStore.new_trace(identifier, deviceID)
    userStore.upsert_user(identifier, last_known_device_id=deviceID)
    
    return {
        'statusCode': 200,
        'body': 'OK'
    }
