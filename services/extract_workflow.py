import shutil
import asyncio

from services.pdfs.retrieve_pdf import download_pdf
from services.images.process_image import combine_alt_text_for_image
from services.collect_tasks import *
from services.texts.generate_text import generate_final_text
from config.constants import PDF_TMP_SAVE_PATH, IMG_TMP_SAVE_PATH, SUCCESS
from schemas.Response import OKResponse, ErrorResponse
from exceptions.exceptions import OpenAIError, MarvinError, AWSError


async def extract_all_contents_from_pdf(pdf_link, enable_image, enable_correct):
    """
    Extract all content in the PDF
    :param pdf_link: the link to PDF file
    :param enable_image: whether to enable image extraction
    :param enable_correct: whether to enable text correction
    :return: extracted text
    """
    # Download the cloud pdf file to local disk
    download_res_msg, local_pdf_file_path, pdf_name = download_pdf(pdf_link)
    # Check the downloading status
    if download_res_msg == SUCCESS:
        collect_res_msg = SUCCESS
        try:
            # Get text and image path list
            text_list, image_path_list = get_text_image_list(local_pdf_file_path, pdf_name)
            # Collect the async tasks
            text_tasks = collect_text_task(text_list, enable_correct)
            image_upload_tasks, image_caption_generating_tasks = collect_image_task(image_path_list, enable_image)

            # use the pre-processed text list (make sure assigned when enable_correct=False)
            corrected_text_result = text_list

            # Execute the async tasks
            if enable_image:
                try:
                    image_link_result = await asyncio.gather(*image_upload_tasks)
                except AWSError as aws_err:
                    # Assign local image path to image_link_result to differentiate page number with the path
                    image_link_result = image_path_list.copy()
                    collect_res_msg = aws_err.message
                try:
                    image_caption_result = await asyncio.gather(*image_caption_generating_tasks)
                except MarvinError as marvin_err:
                    image_caption_result = ["" for _ in image_path_list]
                    collect_res_msg = marvin_err.message

            if enable_correct:
                try:
                    corrected_text_result = await asyncio.gather(*text_tasks)
                except OpenAIError as openai_err:
                    collect_res_msg = openai_err.message

            # Organize the final result
            text_result = f"PDF file link: {pdf_link}\n\n"
            if enable_image:
                # Combine the image alternative text per image link result and image caption result
                image_alt_result = combine_alt_text_for_image(image_link_result, image_caption_result)
                text_result += generate_final_text(corrected_text_result, image_alt_result)
            else:
                text_result += generate_final_text(corrected_text_result)

            # Clean up the temporary folder and files
            os.remove(f"{PDF_TMP_SAVE_PATH}{pdf_name}.pdf")
            shutil.rmtree(f"{IMG_TMP_SAVE_PATH}/{pdf_name}")
        except Exception as err:
            return ErrorResponse(msg=f"Unknown err: {err}")

        if collect_res_msg != SUCCESS:  # return partial content
            return OKResponse(code=206, data=text_result, msg=collect_res_msg)  # partial content
        else:  # completely succeeded
            return OKResponse(data=text_result)
    else:  # downloading pdf failed
        return ErrorResponse(msg=download_res_msg)
