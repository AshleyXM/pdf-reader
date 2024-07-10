import os
from dotenv import load_dotenv

# load env var
load_dotenv()

# read environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_IMAGE_BUCKET = os.getenv('AWS_IMAGE_BUCKET')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

IMG_TMP_SAVE_PATH = os.getenv('IMG_TMP_SAVE_PATH')
PDF_TMP_SAVE_PATH = os.getenv('PDF_TMP_SAVE_PATH')

# request status
SUCCESS = "success"
