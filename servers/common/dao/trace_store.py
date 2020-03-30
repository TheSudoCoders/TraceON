import boto3
from boto3.dynamodb.conditions import Attr, And
from common.utils import disable_keyword_argument_on_none, time_now_standard

ATTR_CREATED_AT = 'createdAt'
ATTR_UPDATED_AT = 'updatedAt'
ATTR_DEVICE_ID = 'deviceID'
ATTR_FACE_HASH = 'faceHash'
ATTR_EVENT_ID = 'eventID'


class TraceStore:
    def __init__(self, tablename):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(tablename)

    def new_trace(self, eventID, deviceID):
        self.table.update_item(
            Key={
                ATTR_EVENT_ID: eventID,
            },
            UpdateExpression="SET #attr_device_id = :device_id, #attr_created_at = if_not_exists(#attr_created_at, :time_now), #attr_updated_at = :time_now",
            ExpressionAttributeNames={
                "#attr_device_id": ATTR_DEVICE_ID,
                "#attr_created_at": ATTR_CREATED_AT,
                "#attr_updated_at": ATTR_UPDATED_AT
            },
            ExpressionAttributeValues={
                ":device_id": deviceID,
                ":time_now": time_now_standard()
            },
        )

    def upsert_user_for_trace(self, eventID, facehash):
        self.table.update_item(
            Key={
                ATTR_EVENT_ID: eventID,
            },
            UpdateExpression="SET #attr_face_hash = if_not_exists(#attr_face_hash, :face_hash), #attr_updated_at = :time_now",
            ExpressionAttributeNames={
                "#attr_face_hash": ATTR_FACE_HASH,
                "#attr_updated_at": ATTR_UPDATED_AT
            },
            ExpressionAttributeValues={
                ":face_hash": facehash,
                ":time_now": time_now_standard()
            },
        )

    def list_event_ids_for_facehash(self, facehash):
        fe = Attr(ATTR_FACE_HASH).eq(facehash)
        first_pass = True
        last_evaluated_key = None

        scan = disable_keyword_argument_on_none(self.table.scan)
        while last_evaluated_key or first_pass:
            scan_results = scan(
                ProjectionExpression='{:s},{:s}'.format(ATTR_EVENT_ID, ATTR_UPDATED_AT),
                FilterExpression=fe,
                ExclusiveStartKey=last_evaluated_key
            )
            first_pass = False

            if 'LastEvaluatedKey' in scan_results:
                last_evaluated_key = scan_results['LastEvaluatedKey']
            else:
                last_evaluated_key = None
                
            for item in scan_results['Items']:
                yield {
                    'eventID': item[ATTR_EVENT_ID],
                    'updatedAt': item[ATTR_UPDATED_AT]
                }

    def get_device_contacts_time_range(self, facehash, date_range):
        start_date = date_range['start_date']
        end_date = date_range['end_date']
        
        fe = Attr(ATTR_FACE_HASH).eq(facehash) & Attr(ATTR_CREATED_AT).between(start_date, end_date)
        last_evaluated_key = None
        first_pass = True

        scan = disable_keyword_argument_on_none(self.table.scan)
        
        while last_evaluated_key or first_pass:
            scan_results = scan(
                ProjectionExpression='{:s},{:s}'.format(ATTR_DEVICE_ID, ATTR_CREATED_AT),
                FilterExpression=fe,
                ExclusiveStartKey=last_evaluated_key
            )
            first_pass = False

            if 'LastEvaluatedKey' in scan_results:
                last_evaluated_key = scan_results['LastEvaluatedKey']
            else:
                last_evaluated_key = None

            for item in scan_results['Items']:
                # NOTE: redeclared for documentation purposes
                yield {
                    'deviceID': item[ATTR_DEVICE_ID],
                    'createdAt': item[ATTR_CREATED_AT]
                }

    def get_facehash_contacts_from_device_id_and_time_range(self, deviceid, date_range):
        start_date = date_range['start_date']
        end_date = date_range['end_date']

        fe = Attr(ATTR_DEVICE_ID).eq(deviceid) & Attr(ATTR_CREATED_AT).between(start_date, end_date)
        last_evaluated_key = None
        first_pass = True

        scan = disable_keyword_argument_on_none(self.table.scan)

        while last_evaluated_key or first_pass:
            scan_results = scan(
                ProjectionExpression='{:s},{:s}'.format(ATTR_FACE_HASH, ATTR_UPDATED_AT),
                FilterExpression=fe,
                ExclusiveStartKey=last_evaluated_key
            )
            first_pass = False

            if 'LastEvaluatedKey' in scan_results:
                last_evaluated_key = scan_results['LastEvaluatedKey']
            else:
                last_evaluated_key = None
                
            for item in scan_results['Items']:
                if ATTR_FACE_HASH not in item:
                    continue

                yield {
                    'faceHash': item[ATTR_FACE_HASH],
                    'interactedOn': item[ATTR_UPDATED_AT]
                }
