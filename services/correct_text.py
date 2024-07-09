import re
from helpers.openai_helper import async_correct_text_with_openai

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
            if 'A' <= ch <= 'Z':  # there is newline ahead, current character is cap word => new paragraph
                current_page_text += '\n' + ch
                has_new_line = False
            elif 'a' <= ch <= 'z':  # there is newline ahead, current character is small word => x newline semantically
                current_page_text += " " + ch
                has_new_line = False
            elif ch == '\n':  # two newline in a row
                continue  # has_new_line=True, continue to check the next character
            else:  # there is newline ahead, the current character is digit or other unknown character
                current_page_text += '\n' + ch
                has_new_line = False
        else:  # no newline before, write the current character
            current_page_text += ch

    return text


async def correct_text_with_openai(text):
    """
    Call OpenAI API to fix spacing error in the extracted text
    :param text: uncorrected text
    :return: corrected text via OpenAI model
    """
    response = await async_correct_text_with_openai(
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
        corrected_text = response.choices[0].message.content.strip()
    except Exception as e:  # catch all possible exceptions
        print(f"Error occurred in OpenAI correcting text process: {e}")
        # return the original text without crushing
        return text
    else:
        return corrected_text
