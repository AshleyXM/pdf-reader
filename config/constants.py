import os
from dotenv import load_dotenv

# load env var
load_dotenv()

# read environment variables
AWS_REGION = os.getenv('AWS_REGION')
AWS_IMAGE_BUCKET = os.getenv('AWS_IMAGE_BUCKET')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

IMG_TMP_SAVE_PATH = os.getenv('IMG_TMP_SAVE_PATH')
PDF_TMP_SAVE_PATH = os.getenv('PDF_TMP_SAVE_PATH')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

# Token related
TOKEN_FIELD_1 = os.getenv('TOKEN_FIELD_1')
TOKEN_FIELD_2 = os.getenv('TOKEN_FIELD_2')
TOKEN_FIELD_1_VAL = os.getenv('TOKEN_FIELD_1_VAL')
TOKEN_FIELD_2_VAL = os.getenv('TOKEN_FIELD_2_VAL')

# Working directory in lambda function
LAMBDA_TASK_ROOT = os.getenv('LAMBDA_TASK_ROOT')

# request status
SUCCESS = "success"
