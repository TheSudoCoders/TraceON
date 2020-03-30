import json


def handle_device(event, traceStore):
    # TODO(james): Get data from within a time range.
    # I'm getting all the data now to save some time

    queryParams = event['queryStringParameters']
    deviceID = queryParams['deviceID']

    events = [event for event in traceStore.list_trace_events_for_device(deviceID)]
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(events)
    }
