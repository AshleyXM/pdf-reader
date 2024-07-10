# PDF Reader

This project aims to serve as middleware between an original PDF file and being used to construct knowledge base in [dify](https://dify.ai/). However, I hope it does more than that.


### Feature and Performance Comparison

|                  | PDF Reader                                                                               | Jina Reader                                                                    | Amazon Textract                                                                          |
|------------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Response Speed   | Fast (*)                                                                                 | Very Fast                                                                      | Very Fast                                                                                |
| Response Content | Text + Image (JSON format)                                                               | Text                                                                           | Text + Image                                                                             |
| Pros             | Extra features: 1. Image alternative text  2. Text correction                            | The response speed for text extraction is fast and the accuracy is acceptable. | The response contains text and image result and the response speed is fast.              |
| Cons             | It takes longer response time if enabling image extraction and text correction function. | No image extraction; accuracy of text result is not high enough.               | The content of text and image messed up when they are not arranged strictly vertically . |
| Local Deployment | ✅                                                                                        | ❌                                                                              | ❌                                                                                        |
| Open Source      | ✅                                                                                        | 🤔 (Partial)                                                                   | ❌                                                                                        |

Note (*): PDF Reader can reach the same fast speed as Jina Reader if query parameters `image=False` and `correct=False` were set, which disable the two time-consuming features.

## Request Query Parameters
- `image`: Decides on whether to enable generating alternative texts for images in PDF files. It defaults to be True. If you don't want this feature, you can set `image=false` or `image=False` (case of bool value does not matter).
- `correct`: Decides on whether to enable text correction for text in PDF files. By enabling this feature, the text accuracy would improve by 20% by fixing some spacing and typographical errors. However, it would take longer time to process. You can set `correct=false` or `correct=False` to disable it.

### Usage Example
Local: `http://127.0.0.1:8000/[PDF link]?correct=false&image=false`
Cloud: `http://[Hosted address]/[PDF link]?correct=false&image=false`

## Response Fields
1. `code`: Status code for current request.
   - `200`: Request success.
   - `206`: Request partial success, which means part of response can be returned, but some functionality did not work (like image uploading to S3, image caption generation and text correction).
   - `400`: Request error.
2. `data`: Extracted content from PDF file, by default including corrected text and alternative text for images. It depends on the query parameters and running status of services under the hood.
3. `msg`: Response message. When all the services ran successfully, it would be "success", otherwise, there would be some explanation message.

## How to Set up
1. Download the repo:
```bash
git clone https://github.com/AshleyXM/pdf-reader.git
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Apply for some API keys

What you will need:
   1. AWS Access Key and Secret Access Key
   2. AWS S3 Bucket Name
   3. OpenAI API key

Then, run the below command and replace mine with the keys you applied in `.env` file:

```bash
cp .env.example .env
```

🎉🎉🎉 Congrats! You are good to go now!

## How to Run
Run the below command:
```bash
uvicorn app.main:app --reload
```

Access http://127.0.0.1:8000/ with your browser, and you'll see the home page, which displays some quick guides of the project.

## Highlights
- Developed middleware hosted on AWS Lambda using Python FastAPI to facilitate the knowledge base construction from PDF files for customized GPTs in Stanford courses.
- Stored images in AWS S3 to obtain public links and generated alternative text for images in the format `[image caption](image link)`.
- Improved text extraction accuracy by 20% by leveraging OpenAI Vision Model to correct spacing and typographical errors.
- Optimized response speed by 67% with asynchronous processing with text correction and image alternative text generation.
- Enhanced project robustness and reliability by implementing exception handling and extensive test cases. (still working on)


## Challenges
One of the biggest challenges is how to optimize the response speed. 

At first, I just utilized **Azure Computer Vision** to get caption and OCR result of each image and leveraged **OpenAI LLM** `gpt-turbo-3.5` to correct the spacing and typographical errors in text content.

However, as the number of pages in PDF file grows, it takes forever to process one PDF file, since even one API call to OpenAI and Azure CV takes several seconds. So I realized that I need to run these tasks parallelly instead of one by one.

Then here came new problem. Even though OpenAI provides asynchronous support, Azure CV still does not implement it. Therefore, in order to get to improve the response speed. I need to make a tradeoff between abandoning the original plan by adding image processing and figuring out another way to do it.

Fortunately, finally I found [marvin](https://www.askmarvin.ai/docs/vision/captioning/#async-support) toolkit which is based on **OpenAI Vision** and provides pretty good asynchronous support for generating image caption.

By trying so hard to do some optimization, then response speed improved by around 67%, which is pretty satisfying for our current task.

