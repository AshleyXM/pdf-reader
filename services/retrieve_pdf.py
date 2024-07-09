import requests
import os

from config.constants import PDF_TMP_SAVE_PATH


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
    status = "success"  # the status of downloading the pdf
    file_save_path = ""
    pdf_name = ""
    try:
        response = requests.get(pdf_url)
        # Only support pdf file parsing
        if response.headers.get("Content-Type") == "application/pdf":
            response.raise_for_status()  # raise exception if the status code is 4xx or 5xx
            pdf_name = pdf_url.split("/")[-1].split(".")[0]  # only get the filename (avoid extension missing case)
            if not os.path.exists(PDF_TMP_SAVE_PATH):
                os.makedirs(PDF_TMP_SAVE_PATH)
            file_save_path = f"{PDF_TMP_SAVE_PATH}{pdf_name}.pdf"
            with open(file_save_path, 'wb') as file:
                file.write(response.content)
            print(f"PDF has been saved to {file_save_path}")
        else:  # not a pdf file
            print("Please make sure the link is a pdf file.")
            status = "Invalid pdf link, please check again..."
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")  # HTTP error
        status = "HTTP error during pdf downloading!"
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")  # other request error
        status = "Request error during pdf downloading!"
    finally:
        return status, file_save_path, pdf_name
