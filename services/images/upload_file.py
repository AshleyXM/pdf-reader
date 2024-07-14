from botocore.exceptions import NoCredentialsError
import asyncio

from helpers.singleton_clients import s3_client
from config.constants import AWS_IMAGE_BUCKET, AWS_REGION
from exceptions.exceptions import AWSError


IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'gif', 'tiff', 'webp', "bmp", "svg", "psd"]


async def upload_image(local_image_path):
    """
    Upload image to AWS S3
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
    # print(f"Image bucket_key: {bucket_key}")
    try:
        # upload the image to S3 image bucket (sync method)
        # s3_client.upload_file(local_image_path, AWS_IMAGE_BUCKET, bucket_key,
        #                       ExtraArgs={'ContentType': f"image/{file_type}", 'ACL': 'public-read'})
        # Upload image to S3 asynchronously
        await asyncio.to_thread(s3_client.upload_file, local_image_path, AWS_IMAGE_BUCKET, bucket_key,
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
        return file_url


# Async image uploading method
async def get_image_link(local_image_path):
    try:
        image_link = await upload_image(local_image_path)
    except Exception as err:
        raise AWSError(message=f"Error in getting image link: {err}")
    return image_link
