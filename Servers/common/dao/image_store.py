import boto3
import base64
import os
from . import utils

IMAGE_EXTENSION = "jpg"


class ImageStore:
    def __init__(self, s3_bucketname):
        self.s3 = boto3.resource('s3')
        self.client = self.s3.Bucket(s3_bucketname)

    def list(self, identifier):
        return utils.remove_directories(
            utils.extract_key_with_identifier_from_ObjectSummary(
                identifier,
                self.client.objects.all()
            )
        )

    def append(self, identifier, base64img):
        indexedFiles = self.list(identifier)
        indexedFiles.sort()

        sequenceNo = 1
        if len(indexedFiles) > 0:
            sequenceNo = int(os.path.basename(os.path.splitext(indexedFiles[-1])[0]))
            sequenceNo += 1

        imageData = base64.b64decode(base64img)
        self.client.put_object(
            Body=imageData,
            Key="{:s}/{:02d}.{:s}".format(identifier, sequenceNo, IMAGE_EXTENSION)
        )
