import datetime
import json


def handle_trace(event, traceStore, userStore):
    if 'queryStringParameters' not in event or event['queryStringParameters'] is None:
        return {
            'statusCode': 400,
            'body': 'Bad Request'
        }

    queryParams = event['queryStringParameters']
    userFaceHash = queryParams['faceHash']
    startDate = queryParams['startDate']
    endDate = queryParams['endDate']
    stride = 120 # NOTE: Default specified by api.yml

    if userFaceHash.strip() == "" or userStore.get_user(userFaceHash) is None:
        return {
            'statusCode': 404,
            'body': 'Not found'
        }
    
    if 'stride' in queryParams and queryParams['stride'] is not None:
        stride = int(queryParams['stride'])

    devices = traceStore.get_device_contacts_time_range(userFaceHash, {
        'start_date': startDate,
        'end_date': endDate
    })
    contactFaceHashList = []
    for device in devices:
        timeContacted = datetime.datetime.strptime(device['createdAt'], "%Y-%m-%dT%H:%M:%S")
        timeDelta = datetime.timedelta(minutes=stride/2)
        timeBegin = timeContacted - timeDelta
        timeEnd = timeContacted + timeDelta

        faceHashes = traceStore.get_facehash_contacts_from_device_id_and_time_range(device['deviceID'], {
            'start_date': timeBegin.strftime("%Y-%m-%dT%H:%M:%S%Z"),
            'end_date': timeEnd.strftime("%Y-%m-%dT%H:%M:%S%Z"),
        })
        for faceHash in faceHashes:
            contactFaceHashList.append({
                'deviceID': device['deviceID'],
                'faceHash': faceHash['faceHash'],
                'interactedOn': faceHash['interactedOn']
            })

    contacts = []
    isDirectContact = False
    for contactFaceHash in contactFaceHashList:
        user = userStore.get_user(contactFaceHash['faceHash'])
        if user['isConfirmedCase']:
            isDirectContact = True
            
        if user['faceHash'] == userFaceHash:
            print(user['faceHash'])
            continue # NOTE: Oh no, we got into contact with ourselves!

        contacts.append({
            'faceHash': user['faceHash'],
            'lastKnownDeviceID': user['lastKnownDeviceID'],
            'isConfirmedCase': bool(user['isConfirmedCase']),
            'interactedDevice': contactFaceHash['deviceID'],
            'interactedOn': contactFaceHash['interactedOn']
        })

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'tracees': contacts,
            'isDirectContact': isDirectContact
        })
    }
