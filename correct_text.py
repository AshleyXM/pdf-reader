import re
import openai
import os
from dotenv import load_dotenv

# load env var
load_dotenv()
# read environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set OpenAI api key
openai.api_key = OPENAI_API_KEY
# Specify model to use
GPT_MODEL = "gpt-3.5-turbo"  # model name


def preprocess_text(text):
    """
    Pre-process the text by removing extra spaces or newline
    :param text: uncorrected text
    :return: corrected text
    """
    newline_placeholder = "[newline]"
    text = text.replace("\n\n", newline_placeholder)  # avoid the real newline is replaced with a space
    text = re.sub(fr'[\s]*{newline_placeholder}[\s]*', f'{newline_placeholder}', text)  # remove any space near newline
    text = re.sub(r'[\s]+', ' ', text)  # keep only one space (applies to multiple spaces/tabs/newlines)
    text = text.replace(' ,', ',')  # remove space before comma
    text = text.replace(" .", ".")  # remove space before period
    text = text.replace(newline_placeholder, "\n")  # recover the real newline

    return text


def correct_text_with_openai(text):
    """
    Call OpenAI API to fix spacing error in the extracted text
    :param text: uncorrected text
    :return: corrected text via OpenAI model
    """
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that only corrects spacing and typographical errors."},
            {"role": "user",
             "content": f"Do not change the content; only correct spacing and typographical errors for the "
                        f"following text to improve readability. Return only the corrected results.\n\n{text}"}
        ],
        max_tokens=2048,  # the max number of token generated
        temperature=0.0,  # restrict the model to have zero creativity
        top_p=1.0,
        n=1,  # chat round
        stop=None  # no specified stopping condition
    )
    try:
        # get corrected text
        corrected_text = response.choices[0].message['content'].strip()
    except:  # catch all possible exceptions
        print("Error occurred during text correction process.")
        # return the original text without crushing
        return text
    else:
        return corrected_text
