import shutil
import io
import fitz
from langchain_community.document_loaders import PyPDFLoader

from retrieve_pdf_from_url import download_pdf
from generate_image_alt_content import generate_image_alt_content
from correct_text import preprocess_text
from correct_text import correct_text_with_openai

import os
from dotenv import load_dotenv

# load env var
load_dotenv()
# read environment variables
IMG_TMP_SAVE_PATH = os.getenv('IMG_TMP_SAVE_PATH')


def extract_page_from_pdf(pdf_name, pdf_document, page_index, page):
    """
    Extract all content of the specified page in the given pdf
    :param pdf_name: the name of pdf being extracted, used as part of the path of the generated image
    :param pdf_document: the page document
    :param page_index: the index of current page (starting from 1)
    :param page: the page object
    :return: the text content within current page, including OCR texts and alternative image texts
    """
    page_content = page.dict()["page_content"]

    preprocessed_content = preprocess_text(page_content)

    # Call openai to correct errors in the content
    # corrected_content = correct_text_with_openai(preprocessed_content)
    corrected_content = preprocessed_content

    current_page_text = f"Page {page_index}\n"  # page header
    current_page_text += corrected_content + "\n"  # page corrected text

    # Extract images at current page
    current_page = pdf_document.load_page(page_index - 1)
    current_page_image_list = current_page.get_images(full=True)
    # Create temporary folder to save images if current page contains images
    tmp_img_output_folder = f"{IMG_TMP_SAVE_PATH}{pdf_name}/page{page_index}"
    if len(current_page_image_list) != 0 and not os.path.exists(tmp_img_output_folder):
        os.makedirs(tmp_img_output_folder)
    # Extract images
    for img_index, img in enumerate(current_page_image_list, start=1):
        xref = img[0]  # get image xref, which is the id of image
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]

        image_path = f"{tmp_img_output_folder}/image_{img_index}.png"  # current image path
        # Save the image locally
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        # Generate alternative text
        image_alt_content = generate_image_alt_content(image_path)
        # Append the current image alt text
        current_page_text += f"\n{image_alt_content}"
    return current_page_text


def extract_all_contents_from_pdf(pdf_link):
    # Download the cloud pdf file to local disk
    local_pdf_file_path, pdf_name = download_pdf(pdf_link)

    # Extract text content from pdf file
    loader = PyPDFLoader(local_pdf_file_path)
    pages = loader.load_and_split()

    # Extract images from pdf file
    pdf_document = fitz.open(local_pdf_file_path)

    text_result = ""

    text_result += f"PDF file link: {pdf_link}\n\n"
    for page_index, page in enumerate(pages, start=1):
        text_result += extract_page_from_pdf(pdf_name, pdf_document, page_index, page)
        text_result += "\n\n"  # Add line space between different pages

    # Clean up the temporary folder and files
    # shutil.rmtree(f"{IMG_TMP_SAVE_PATH}/{pdf_name}")
    print("Extraction succeeded!")
    return text_result
