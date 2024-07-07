import boto3

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials


class SingletonClientMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class S3Client(metaclass=SingletonClientMeta):
    """
    Create Singleton S3 client
    """
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region):
        self.client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

    def get_client(self):
        return self.client


class AzureCVClient(metaclass=SingletonClientMeta):
    """
    Create Singleton Computer Vision client
    """
    def __init__(self, endpoint, subscription_key):
        self.client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    def get_client(self):
        return self.client
