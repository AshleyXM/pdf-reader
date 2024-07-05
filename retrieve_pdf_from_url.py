import requests
import os
from dotenv import load_dotenv

# load env var
load_dotenv()
# read pdf temporary save path
PDF_TMP_SAVE_PATH = os.getenv('PDF_TMP_SAVE_PATH')


def download_pdf(pdf_url):
    """
    Download the pdf file from cloud to local
    :param pdf_url: the url link to the pdf file
    :return: the temporary local path the downloaded file
    """
    try:
        response = requests.get(pdf_url)
        # Only support pdf file parsing
        if response.headers.get("Content-Type") != "application/pdf":
            print("Please make sure the link is a pdf file.")
            return
        response.raise_for_status()  # raise exception if the status code is 4xx or 5xx
        pdf_name = pdf_url.split("/")[-1].split(".")[0]  # only get the filename (avoid extension missing case)
        if not os.path.exists(PDF_TMP_SAVE_PATH):
            os.makedirs(PDF_TMP_SAVE_PATH)
        file_save_path = f"{PDF_TMP_SAVE_PATH}{pdf_name}"
        with open(f"{PDF_TMP_SAVE_PATH}/{pdf_name}.pdf", 'wb') as file:
            file.write(response.content)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")  # HTTP error
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")  # other request error
    else:  # return pdf path if succeeded
        print(f"PDF has been saved to {file_save_path}")
        return file_save_path
