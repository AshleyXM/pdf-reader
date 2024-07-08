import math
import io
from PIL import Image
import marvin


import os
from dotenv import load_dotenv

# load env var
load_dotenv()

# read environment variables
OCR_SUBSCRIPTION_KEY = os.getenv('OCR_SUBSCRIPTION_KEY')
OCR_ENDPOINT = os.getenv('OCR_ENDPOINT')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

marvin.settings.openai.api_key = OPENAI_API_KEY


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


async def get_caption_with_marvin(image_list):
    caption = await marvin.caption_async(image_list)
    return caption


def combine_alt_text_for_image(image_link_list, image_caption_list):
    """
    Generate alternative texts for all images in the PDF
        Example: { "page1": ["link1", "link2"], "page2": ["link1"], ... }
    :param image_link_list: the list of image links
    :param image_caption_list: the list of image captions
    :return: a map with alternative texts for all images
    """
    res = {}
    if len(image_link_list) != len(image_caption_list):
        print("The length of image link list does not match with the length of image caption!")
        return res
    for idx, link in enumerate(image_link_list):
        # link sample: https://coursepals-images.s3.us-west-1.amazonaws.com/pdf3/page1/image_1.png
        page_number = link.split("/")[-2][4:]  # get page number from image link (except substring "page")
        alt_text = f"[{image_caption_list[idx]}]({link})"
        if page_number in res:
            res[page_number].append(alt_text)
        else:
            res[page_number] = [alt_text]
    # print(f"combine_alt_text_for_image: {res}")
    return res

