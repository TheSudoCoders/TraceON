import boto3
from boto3.dynamodb.conditions import Attr
from common.utils import disable_keyword_argument_on_none

ATTR_CREATED_AT = 'createdAt'
ATTR_DEVICE_ID = 'deviceID'
ATTR_FACE_HASH = 'faceHash'


class TraceStore:
    def __init__(self, tablename):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(tablename)

    def get_device_contacts_time_range(self, facehash, date_range):
        start_date = date_range['start_date']
        end_date = date_range['end_date']
        
        fe = Attr(ATTR_FACE_HASH).eq(facehash) and Attr(ATTR_CREATED_AT).between(start_date, end_date)
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

            for item in scan_results['Items']:
                # NOTE: redeclared for documentation purposes
                yield {
                    'deviceID': item[ATTR_DEVICE_ID],
                    'createdAt': item[ATTR_CREATED_AT]
                }

    def get_facehash_contacts_from_device_id_and_time_range(self, deviceid, date_range):
        start_date = date_range['start_date']
        end_date = date_range['end_date']

        fe = Attr(ATTR_DEVICE_ID).eq(deviceid) and Attr(ATTR_CREATED_AT).between(start_date, end_date)
        last_evaluated_key = None
        first_pass = True

        scan = disable_keyword_argument_on_none(self.table.scan)

        while last_evaluated_key or first_pass:
            scan_results = scan(
                ProjectionExpression=ATTR_FACE_HASH,
                FilterExpression=fe,
                ExclusiveStartKey=last_evaluated_key
            )
            first_pass = False

            for item in scan_results['Items']:
                yield item[ATTR_FACE_HASH]
