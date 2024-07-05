import boto3


class SingletonS3ClientMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class S3Client(metaclass=SingletonS3ClientMeta):
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
