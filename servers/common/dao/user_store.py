import boto3
import datetime
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

    def upsert_user(self, facehash, *, last_known_device_id=None, is_confirmed_case=False):
        time_now = datetime.datetime.utcnow()
        iso8601_now = time_now.strftime('%Y-%m-%dT%H:%M:%S%z')

        expressionAttributeNames = {
            '#attr_updated_at': ATTR_UPDATED_AT,
            '#attr_created_at': ATTR_CREATED_AT
        }
        expressionAttributeValues = {
            ':new_datetime': iso8601_now,
        }
        update_subexpr = []
        if last_known_device_id is not None:
            update_subexpr.append('SET #attr_device_id = :new_device_id')
            expressionAttributeNames['#attr_device_id'] = ATTR_LAST_KNOWN_DEVICE_ID
            expressionAttributeValues[':new_device_id'] = last_known_device_id
        if is_confirmed_case is not None:
            update_subexpr.append('#attr_is_confirmed_case = :new_confirmed_case')
            expressionAttributeNames['#attr_is_confirmed_case'] = ATTR_IS_CONFIRMED_CASE
            expressionAttributeValues[':new_confirmed_case'] = is_confirmed_case,
        update_subexpr.append('#attr_updated_at = :new_datetime')
        update_subexpr.append('#attr_created_at = if_not_exists(#attr_created_at, :new_datetime)')
        update_expression = ', '.join(update_subexpr)
        
        self.table.update_item(
            Key={
                ATTR_FACE_HASH: facehash,
            },
            UpdateExpression=update_expression,
             ExpressionAttributeNames=expressionAttributeNames,
            ExpressionAttributeValues=expressionAttributeValues,
        )

    def get_user(self, facehash):
        kce = Key(ATTR_FACE_HASH).eq(facehash)
        query_result = self.table.query(
            KeyConditionExpression=kce,
            ProjectionExpression='{:s},{:s},{:s},{:s},{:s}'.format(ATTR_FACE_HASH, ATTR_IS_CONFIRMED_CASE, ATTR_LAST_KNOWN_DEVICE_ID, ATTR_CREATED_AT, ATTR_UPDATED_AT)
        )

        if int(query_result['Count']):
            return query_result['Items'][0]
        return None
