import math

from utils.singleton_clients import AzureCVClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import time
from utils.upload_file import upload_image

import io

from PIL import Image

import os
from dotenv import load_dotenv

# load env var
load_dotenv()

# read environment variables
OCR_SUBSCRIPTION_KEY = os.getenv('OCR_SUBSCRIPTION_KEY')
OCR_ENDPOINT = os.getenv('OCR_ENDPOINT')

# Create a CV client
azure_cv_client = AzureCVClient(OCR_ENDPOINT, OCR_SUBSCRIPTION_KEY).get_client()


def resize_image_stream(original_image_stream, min_size):
    """
    Return the resized image stream if either width or height < 50, otherwise return the original image stream
    :param original_image_stream: the original image stream
    :param min_size: the width and height threshold
    :return: the resized image stream
    """
    img_obj = Image.open(original_image_stream)  # get the image object
    # Get the width and height of the image
    width, height = img_obj.size
    print(f"width, height: {width, height}")
    # Check image width and height
    if width < min_size or height < min_size:
        ratio = math.ceil(max(min_size / width, min_size / height))  # round up
        new_size = (int(width * ratio), int(height * ratio))
        img_obj = img_obj.resize(new_size, Image.LANCZOS)  # resize the image
        resized_image_stream = io.BytesIO()
        img_obj.save(resized_image_stream, format="png")
        return resized_image_stream

    return original_image_stream


def get_caption_n_text_from_image(local_image_path):
    """
    Get the caption and OCR text from the given image
    :param local_image_path: the local path to the image
    :return: caption_result, ocr_result
    """
    try:
        # Open the image as image stream
        with open(local_image_path, "rb") as image_stream:
            resized_image_stream = resize_image_stream(image_stream, 50)  # azure requires width and height >= 50
            resized_image_stream.seek(0)
            # Call API to generate caption for the image
            caption_response = azure_cv_client.describe_image_in_stream(resized_image_stream)
            # move the pointer to the start
            resized_image_stream.seek(0)
            # Call API to extract texts in the image via OCR
            ocr_response = azure_cv_client.read_in_stream(resized_image_stream, raw=True)

        # get OCR operation URL
        operation_location = ocr_response.headers["Operation-Location"]
        # get the operation ID, from which operation status can be got
        operation_id = operation_location.split("/")[-1]

        ocr_result = ""

        # Poll for OCR result
        while True:
            ocr_status = azure_cv_client.get_read_result(operation_id)  # get the OCR result
            if ocr_status.status not in ['notStarted', 'running']:  # ran and not running now
                if ocr_status.status == OperationStatusCodes.succeeded:  # instead of "failed"
                    read_results = ocr_status.analyze_result.read_results
                    for read_result in read_results:
                        for line in read_result.lines:
                            ocr_result += line.text + " "
                else:
                    print(f"OCR failed for image {local_image_path}...")
                break
            time.sleep(0.5)  # task running, wait for 1s then before checking

        caption_result = ""
        if len(caption_response.captions) == 0:
            print("No caption was found.")
        else:
            # Sort the captions per the confidence, in descending order
            sorted_captions = sorted(caption_response.captions, key=lambda c: c.confidence, reverse=True)
            for caption in sorted_captions:  # use loop to avoid IndexError
                caption_result = caption.text  # set to the caption with the highest confidence
                break
    except FileNotFoundError:
        print(f"{local_image_path} is not found.")
    except:
        print(f"Error occurred during fetching caption and OCR results from image {local_image_path}")
    else:
        return caption_result, ocr_result


def generate_image_alt_content(local_image_path):
    """
    Generate the alternative text for the image
    :param local_image_path: image path
    :return: alternative text
    """
    # Upload the image stream to S3
    image_link = upload_image(local_image_path)
    print(local_image_path)
    caption_result, ocr_result = get_caption_n_text_from_image(local_image_path)
    result = "[{}]({}): {}".format(caption_result, image_link, ocr_result)
    print(f"Image alternative text: {result}")
    return result
