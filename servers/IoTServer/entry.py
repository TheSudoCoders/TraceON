import re
import os
import json
import urllib.request
from common.dao.image_store import ImageStore
from common.dao.user_store import UserStore
from common.dao.trace_store import TraceStore

S3_BUCKET = os.getenv("S3_BUCKET")
USERSTORE_TABLENAME = os.getenv("USERSTORE_TABLENAME")
TRACESTORE_TABLENAME = os.getenv("TRACESTORE_TABLENAME")
ML_SERVER_URL = os.getenv("ML_SERVER_URL")
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
    event_identifier = event['id']
    image = event['image']
    deviceID = event['deviceID']

    # Upload the base64 image as a JPG
    imageStore = ImageStore(S3_BUCKET)
    seq_no = imageStore.append(event_identifier, image)

    # Upsert a new trace
    traceStore.new_trace(event_identifier, deviceID)

    # TODO(james): Improve method to contact the machine learning backend.
    # Some solutions I can think off: Queues or Asynchronous Lambda Rings
    headers = {
        'Content-Type': 'application/json'
    }
    post_data = json.dumps({
        'id': event_identifier,
        'image': imageStore.get_presigned_url(event_identifier, seq_no)
    }).encode()
    print(post_data)
    req = urllib.request.Request(ML_SERVER_URL, data=post_data, headers=headers)
    resp = {}
    with urllib.request.urlopen(req) as response:
        ml_response = response.read()
        resp = json.loads(ml_response)
        if 'id' not in resp or resp['id'] is not event_identifier:
            print("Identifier mismatch, ID lambda: {:s}, ID ML: {:s}".format(event_identifier, resp['id']))
            return {
                'statusCode': 502,
                'body': 'Identifier mismatch'
            }
        
        if 'facehash' not in resp or resp['facehash'] == None:
            print("Facehash not found for Event ID: {:s}".format(event_identifier))
            return {
                'statusCode': 204,
                'body': 'No Content'
            }
    
    # Update user store and trace stores
    traceStore.upsert_user_for_trace(event_identifier, resp['facehash'])
    userStore.upsert_user(resp['facehash'], last_known_device_id=deviceID)
    
    return {
        'statusCode': 200,
        'body': 'OK'
    }
