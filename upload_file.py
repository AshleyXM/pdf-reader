from botocore.exceptions import NoCredentialsError

from s3_client import S3Client

import os
from dotenv import load_dotenv

# load env var
load_dotenv()

# read environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_IMAGE_BUCKET = os.getenv('AWS_IMAGE_BUCKET')


IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'gif', 'tiff', 'webp', "bmp", "svg", "psd"]


# Create Singleton S3 client instance
s3_client = S3Client(
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION
).get_client()


def upload_image(local_image_path):
    """
    Upload image file to AWS S3
    :param local_image_path: path to the file, including the pdf name to which it belongs
    Example: /tmp/image/pdf_name/page_number/image_n.png
    :return: the image link in S3 bucket
    """
    file_type = local_image_path.split('.')[-1]  # get file suffix
    if file_type not in IMAGE_TYPES:
        print("Unsupported image type:", file_type)
        return ""
    image_path_parts = local_image_path.split('/')
    pdf_name = image_path_parts[-3]
    page_number = image_path_parts[-2]
    image_name = image_path_parts[-1]
    bucket_key = pdf_name + "/" + page_number + "/" + image_name  # image path in the bucket
    print(f"Image bucket_key: {bucket_key}")
    try:
        # upload the image to S3 image bucket
        s3_client.upload_file(local_image_path, AWS_IMAGE_BUCKET, bucket_key,
                              ExtraArgs={'ContentType': f"image/{file_type}", 'ACL': 'public-read'})
    except FileNotFoundError:
        print(f"{local_image_path} not found.")
        return ""
    except NoCredentialsError:
        print("Credentials not available.")
        return ""
    else:
        # return image access URL
        file_url = f"https://{AWS_IMAGE_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{bucket_key}"
        print("Image uploaded successfully:", file_url)
        return file_url
