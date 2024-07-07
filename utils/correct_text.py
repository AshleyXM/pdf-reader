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
    # Pre-process text
    text = text.replace(" ,", ",")  # remove space before comma
    text = text.replace(" .", ".")  # remove space before period
    text = text.replace(". \n", ".\n")  # remove space between period and newline
    text = text.replace("\n ", "\n")  # remove space after newline
    text = re.sub(r'[\s]+', ' ', text)

    current_page_text = ""
    has_new_line = False
    for ch in text:
        if ch == '\n':
            has_new_line = True
            continue
        if has_new_line:
            if 'A' <= ch <= 'Z':  # 前面有换行，当前是大写字母 => 新段落
                current_page_text += '\n' + ch
                has_new_line = False
            elif 'a' <= ch <= 'z':  # 前面有换行，当前是小写字母 => 语义上无需换行
                current_page_text += " " + ch
                has_new_line = False
            elif ch == '\n':  # 连续两个换行
                continue  # has_new_line仍未True，继续判断下一个字符
            else:  # 前面有换行，当前字符是数字或其他未知字符
                current_page_text += '\n' + ch
                has_new_line = False
        else:  # 前面没有换行，直接写入当前字符
            current_page_text += ch

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
             "content": f"Only fix spacing and typographical errors for the below texts to enhance readability "
                        f"but do not change the content, return only the results, do not say anything else.\n\n{text}"}
        ],
        max_tokens=2000,  # the max number of token generated
        temperature=0.0,  # restrict the model to have zero creativity
        top_p=1.0,
        n=1,  # chat round
        stop=None  # no specified stopping condition
    )
    try:
        # get corrected text
        corrected_text = response.choices[0].message['content'].strip()
    except:  # catch all possible exceptions
        print("Error occurred in OpenAI correcting text process.")
        # return the original text without crushing
        return text
    else:
        return corrected_text
