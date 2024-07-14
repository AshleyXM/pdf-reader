import boto3


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
    def __init__(self):
        self.client = boto3.client('s3')

    def get_client(self):
        return self.client


# Create Singleton S3 client instance
s3_client = S3Client().get_client()
