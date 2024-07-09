import os
import shutil
import asyncio

from services.retrieve_pdf import download_pdf
from services.process_image import combine_alt_text_for_image
from services.collect_async_tasks import collect_async_tasks
from config.constants import PDF_TMP_SAVE_PATH, IMG_TMP_SAVE_PATH
from schemas.Response import Response


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
    if download_res_msg == "success":
        # Collect the async tasks
        image_upload_tasks, image_caption_generating_tasks, text_tasks = \
            collect_async_tasks(local_pdf_file_path, pdf_name, enable_image, enable_correct)
        # Execute the async tasks
        if enable_image:
            image_link_result = await asyncio.gather(*image_upload_tasks)
            image_caption_result = await asyncio.gather(*image_caption_generating_tasks)
            # Combine the image alternative text per image link result and image caption result
            image_alt_result = combine_alt_text_for_image(image_link_result, image_caption_result)

        if enable_correct:
            corrected_text_result = await asyncio.gather(*text_tasks)
        else:  # use the pre-processed text list
            corrected_text_result = text_tasks

        text_result = f"PDF file link: {pdf_link}\n\n"
        if enable_image:
            for idx, text in enumerate(corrected_text_result, start=1):
                text_result += f"\nPage{idx}\n"  # add page header
                text_result += f"{text}\n"  # add page text content
                if idx in image_alt_result:
                    for alt_txt in image_alt_result[idx]:
                        text_result += f"{alt_txt}\n"  # add page image alternative text
                text_result += "\n"  # add line space between pages
        else:
            for idx, text in enumerate(corrected_text_result, start=1):
                text_result += f"\nPage{idx}\n"  # add page header
                text_result += f"{text}\n"  # add page text content
                text_result += "\n"  # add line space between pages

        # Clean up the temporary folder and files
        os.remove(f"{PDF_TMP_SAVE_PATH}{pdf_name}.pdf")
        shutil.rmtree(f"{IMG_TMP_SAVE_PATH}/{pdf_name}")
        return Response(code=200, data=text_result, msg=download_res_msg)
    else:  # downloading pdf failed
        return Response(code=400, data="", msg=download_res_msg)
