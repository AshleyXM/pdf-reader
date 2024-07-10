import math
import io
from PIL import Image
import marvin

from config.constants import OPENAI_API_KEY
from exceptions.exceptions import MarvinError

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
    try:
        caption = await marvin.caption_async(image_list)
    except Exception as err:
        raise MarvinError(message=f"Error in generating image caption: {err}")
    return caption


def combine_alt_text_for_image(image_link_list, image_caption_list):
    """
    Generate alternative texts for all images in the PDF
        Example: { "page1": ["link1", "link2"], "page2": ["link1"], ... }
    :param image_link_list: the list of image links
        [[page1_image1, page1_image2], [page6_image1], [page8_image1, page8_image2]]
        link example: https:// or /tmp/image/pdf_name/page_number/image_name (if error happened while uploading)
    :param image_caption_list: the list of image captions
    :return: a map with alternative texts for all images
    """
    res = {}

    # 1. image_link_list https link -> [caption](link)
    # 2. image_link_list local path -> [caption]()
    for idx, link in enumerate(image_link_list):
        # link sample: https://coursepals-images.s3.us-west-1.amazonaws.com/pdf3/page1/image_1.png
        page_number = int(link.split("/")[-2][4:])  # get page number from image link (except substring "page")
        if link.startswith("https"):  # uploading image succeeded
            alt_text = f"[{image_caption_list[idx]}]({link})"
        else:  # image uploading error
            alt_text = f"[{image_caption_list[idx]}]()"
        if page_number in res:
            res[page_number].append(alt_text)
        else:
            res[page_number] = [alt_text]
    # print("The length of image link list does not match with the length of image caption!")
    return res
