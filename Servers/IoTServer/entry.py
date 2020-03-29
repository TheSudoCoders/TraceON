import re
import os
from common.image_store import ImageStore

S3_BUCKET = os.getenv("S3_BUCKET")


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

    identifier = event['id']
    image = event['image']
    
    imageStore = ImageStore(S3_BUCKET)
    imageStore.append(identifier, image)
    
    return {
        'statusCode': 200,
        'body': 'OK'
    }
