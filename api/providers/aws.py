import boto3
from botocore.exceptions import ClientError
from config import BUCKET_NAME
import logging

logging.getLogger(__name__)

class S3:

    def __init__(self, bucket_name=BUCKET_NAME):
        session = boto3.Session()
        self.s3_client = session.client('s3')
        self.bucket_name = bucket_name

    def put_object(self, object_key, content) -> None:
        """
        Put object in s3 based on a file content

        :param object_key: The object key to identify the uploaded object.
        :param content: File content.
        :return: None
        """
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=object_key, Body=content)
        except ClientError as e:
            raise Exception("Could not upload object {} on bucket {} - {}".format(
                object_key, self.bucket_name, e.response['Error']['Code']))
        except Exception as e:
            raise Exception("Could not upload object {} on bucket {} - {}".format(
                object_key, self.bucket_name, e))

    def generate_presigned_url(self, object_key: str, expiration: int=86400) -> str:
        """
        Generate a presigned URL to share time-limited permission to download the objects.

        :param object_key: The object key to identify the uploaded object.
        :param expiration: The number of seconds the presigned URL is valid.
        :return: A dictionary that contains the URL and form fields that contain
                 required access data.
        """
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': self.bucket_name,
                                                                     'Key': object_key},
                                                             ExpiresIn=expiration)
            return response
        except ClientError as e:
            raise Exception("Could not get a presigned URL for bucket {} and object {} - {}".format(
                self.bucket_name, object_key, e.response['Error']['Code']))
        except Exception as e:
            raise Exception("Could not get a presigned URL for bucket {} and object {} - {}".format(
                self.bucket_name, object_key, e))

    def generate_presigned_post(self, object_key: str, expiration: int=10) -> dict:
        """
        Generate a presigned S3 POST request to upload a file.

        :param object_key: The object key to identify the uploaded object.
        :param expiration: The number of seconds the presigned POST is valid.
        :return: A dictionary that contains the URL and form fields that contain
                 required access data.
        """
        try:
            response = self.s3_client.generate_presigned_post(
                Bucket=self.bucket_name, Key=object_key, ExpiresIn=expiration)
            logging.info("Got presigned POST URL: %s", response['url'])
            return response
        except ClientError as e:
            raise Exception("Could not get a presigned POST URL for bucket {} and object {} - {}".format(
                self.bucket_name, object_key, e.response['Error']['Code']))
        except Exception as e:
            raise Exception("Could not get a presigned POST URL for bucket {} and object {} - {}".format(
                self.bucket_name, object_key, e))
