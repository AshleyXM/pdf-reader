import requests
import os
import time

from config.constants import PDF_TMP_SAVE_PATH, AWS_IMAGE_BUCKET, SUCCESS
from helpers.singleton_clients import s3_client


def check_pdf_name_exists(pdf_name):
    """
    Check whether the given pdf name exists in the image bucket
    :param pdf_name: the name of PDF file
    :return: bool value, True for existing, False for not existing
    """
    try:
        response = s3_client.list_objects_v2(Bucket=AWS_IMAGE_BUCKET, Prefix=pdf_name, MaxKeys=1)
        if 'Contents' in response:  # duplicate pdf name
            return True
        else:  # the pdf name does not exist for now
            return False
    except Exception as e:
        print(f"An error occurred while checking key name in S3 bucket: {e}")
        return True


def generate_pdf_key(pdf_name):
    """
    Generate the key stored in image bucket
    :param pdf_name: the name of PDF file
    :return: the original PDF name if the name does not exist in image bucket for now,
            otherwise generate a new key with "-{number}" suffix to differentiate
    """
    if not check_pdf_name_exists(pdf_name):
        return pdf_name
    else:  # duplicate pdf key name
        num = 1  # extra suffix added to pdf name
        while True:
            key_name = f"{pdf_name}-{num}"
            if not check_pdf_name_exists(key_name):
                print(f"Duplicate pdf name: {pdf_name}, renamed to {key_name}")
                return key_name
            num += 1
            if num > 100:  # unknown error / too many duplicates with this pdf name, return the current timestamp
                return f"{pdf_name}-{int(time.time())}"


def download_pdf(pdf_url):
    """
    Download the pdf file from cloud to local disk
    :param pdf_url: the url link to the pdf file
    :return: the status of downloading, the temporary local path the downloaded file, the name of pdf file
        if downloading succeeded, return "success";
        else if the link is not a pdf, return "Invalid pdf link"
        else if issues happened with HTTP, return "HTTP error"
        else, return "Request error"
    """
    msg = SUCCESS  # the status of downloading the pdf
    file_save_path = ""
    pdf_name = ""
    try:
        response = requests.get(pdf_url)
        # Only support pdf file parsing
        if response.headers.get("Content-Type") == "application/pdf":
            response.raise_for_status()  # raise exception if the status code is 4xx or 5xx
            pdf_name = pdf_url.split("/")[-1].split(".")[0]  # only get the filename (avoid extension missing case)
            pdf_name = generate_pdf_key(pdf_name)  # check name duplicity, if duplicate -> rename
            if not os.path.exists(PDF_TMP_SAVE_PATH):
                os.makedirs(PDF_TMP_SAVE_PATH)
            file_save_path = f"{PDF_TMP_SAVE_PATH}{pdf_name}.pdf"
            with open(file_save_path, 'wb') as file:
                file.write(response.content)
        else:  # not a pdf file
            msg = f"Invalid pdf link: {pdf_url}"
    except requests.exceptions.HTTPError as http_err:  # HTTP error
        msg = f"HTTP error during pdf downloading: {http_err}"
    except requests.exceptions.RequestException as req_err:  # Request error, like network error
        msg = f"Request error during pdf downloading: {req_err}"
    except Exception as err:
        msg = f"Unknown error during pdf downloading: {err}"
    finally:
        return msg, file_save_path, pdf_name
