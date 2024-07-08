import asyncio
import concurrent.futures
import functools
import openai
import os
from dotenv import load_dotenv

# load env var
load_dotenv()
# read environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set OpenAI api key
openai.api_key = OPENAI_API_KEY


# sync function, executing OpenAI API call
def call_openai_api(*args, **kwargs):
    return openai.chat.completions.create(*args, **kwargs)


# async function, using thread pool to execute sync OpenAI API call
async def async_correct_text_with_openai(*args, **kwargs):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        # Use functools.partial to create function with partial arguments
        partial_call = functools.partial(call_openai_api, *args, **kwargs)
        response = await loop.run_in_executor(pool, partial_call)
    return response
