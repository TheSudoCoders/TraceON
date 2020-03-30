import boto3
import json


def create_presigned_urls(imageStore, image_keys):
    presigned_urls = []
    for image_key in image_keys:
        s3_client = boto3.client('s3')
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': imageStore.client.name,
                                                                'Key': image_key}, ExpiresIn=3600)
        except ClientError as e:
            print("Erorr while generating presigned URL for key: {:s}".format(image_key))

        presigned_urls.append(response)
    return presigned_urls


def handle_images(event, imageStore, traceStore):
    if 'queryStringParameters' not in event or event['queryStringParameters'] is None:
        return {
            'statusCode': 400,
            'body': 'Bad Request'
        }

    queryParams = event['queryStringParameters']
    userFaceHash = queryParams['faceHash']

    eventIDs = traceStore.list_event_ids_for_facehash(userFaceHash)
    recentEventID = max(eventIDs, key=lambda x: x['updatedAt'])

    if recentEventID is None:
        return {
            'statusCode': 404,
            'body': 'Not found'
        }

    image_keys = imageStore.list(recentEventID['eventID'])
    presigned_urls = create_presigned_urls(imageStore, image_keys)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(presigned_urls)
    }
    
