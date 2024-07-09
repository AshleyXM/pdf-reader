from langchain_community.document_loaders import PyPDFLoader
import fitz
import marvin
import os

from services.process_image import get_caption_with_marvin
from services.correct_text import *
from services.upload_file import get_image_link
from config.constants import IMG_TMP_SAVE_PATH


def collect_page_image_list(pdf_name, pdf_document, page_index):
    """
    Collect the image path list for the current page in PDF file
    :param pdf_name: the name of PDF file
    :param pdf_document: the pdf document
    :param page_index: the page index
    :return: image list of the current page
    """
    # Extract images at current page
    current_page = pdf_document.load_page(page_index - 1)
    current_page_image_list = current_page.get_images(full=True)
    # Create temporary folder to save images if current page contains images
    tmp_img_output_folder = f"{IMG_TMP_SAVE_PATH}{pdf_name}/page{page_index}"
    if len(current_page_image_list) != 0 and not os.path.exists(tmp_img_output_folder):
        os.makedirs(tmp_img_output_folder)
    current_page_image_path_list = []
    # Extract images
    for img_index, img in enumerate(current_page_image_list, start=1):
        xref = img[0]  # get image xref, which is the id of image
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]

        image_path = f"{tmp_img_output_folder}/image_{img_index}.png"  # current image path
        # Save the image locally
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        current_page_image_path_list.append(image_path)
    return current_page_image_path_list


def collect_page_text_list(page_document):
    """
    Get the content in each page and pre-process it
    :param page_document: the page document
    :return: the pre-processed text
    """
    page_content = page_document.dict()["page_content"]
    preprocessed_content = preprocess_text(page_content)
    return preprocessed_content


def collect_async_tasks(local_pdf_file_path, pdf_name, enable_image, enable_correct):
    """
    Get asynchronous tasks for uploading images, generating image captions and correcting text
    :param local_pdf_file_path: local path to the downloaded paf file
    :param pdf_name: the name of pdf file
    :param enable_image: whether to enable image extraction
    :param enable_correct: whether to enable text correction
    :return: image_upload_tasks, image_caption_generating_tasks, text_correction_tasks
    """
    # Extract text content from pdf file
    print(local_pdf_file_path)
    pdf_loader = PyPDFLoader(local_pdf_file_path)
    document_list = pdf_loader.load_and_split()  # load documents and split into chunks

    # Extract images from pdf file
    pdf_document = fitz.open(local_pdf_file_path)

    text_list = []  # store the text in each page
    image_path_list = []

    for page_index, page_document in enumerate(document_list, start=1):
        text_list.append(collect_page_text_list(page_document))
        current_page_image_path_list = collect_page_image_list(pdf_name, pdf_document, page_index)
        image_path_list.append(current_page_image_path_list)

    image_upload_tasks = []
    image_caption_generating_tasks = []
    text_tasks = text_list

    if enable_image:
        # Get asynchronous image uploading tasks
        image_upload_tasks = [get_image_link(path) for page_path_list in image_path_list for path in page_path_list]
        # Convert the local image path list into marvin Image path list
        marvin_image_path_list = [[marvin.Image.from_path(image_path)]
                                  for page_image_path_list in image_path_list
                                  for image_path in page_image_path_list]
        # Get asynchronous image caption generating tasks
        image_caption_generating_tasks = [get_caption_with_marvin(page_image_path_list)
                                          for page_image_path_list in marvin_image_path_list]

    if enable_correct:
        # Get asynchronous text correction tasks
        text_tasks = [correct_text_with_openai(text) for text in text_list]

    return image_upload_tasks, image_caption_generating_tasks, text_tasks
