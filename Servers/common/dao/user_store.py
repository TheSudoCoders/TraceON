import boto3
from boto3.dynamodb.conditions import Key

ATTR_FACE_HASH = 'faceHash'
ATTR_IS_CONFIRMED_CASE = 'isConfirmedCase'
ATTR_LAST_KNOWN_DEVICE_ID = 'lastKnownDeviceID'
ATTR_UPDATED_AT = 'updatedAt'
ATTR_CREATED_AT = 'createdAt'


class UserStore:
    def __init__(self, tablename):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(tablename)

    def get_user(self, facehash):
        kce = Key(ATTR_FACE_HASH).eq(facehash)
        query_result = self.table.query(
            KeyConditionExpression=kce,
            ProjectionExpression='{:s},{:s},{:s},{:s},{:s}'.format(ATTR_FACE_HASH, ATTR_IS_CONFIRMED_CASE, ATTR_LAST_KNOWN_DEVICE_ID, ATTR_CREATED_AT, ATTR_UPDATED_AT)
        )

        if int(query_result['Count']):
            return query_result['Items'][0]
        return None
