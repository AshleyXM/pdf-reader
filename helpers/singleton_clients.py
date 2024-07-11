import boto3

from config.constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION


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


# Create Singleton S3 client instance
s3_client = S3Client(
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION
).get_client()
