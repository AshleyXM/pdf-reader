# pdf-reader

## Introduction
This project aims to serve as middleware between an original PDF file and being used to construct knowledge base in [dify](https://dify.ai/). However, I hope it has more than that.


## Highlights
- Leveraged Langchain PyPDFLoader to process PDF document in chunks.
- Utilized OCR to extract text content from PDF file.
- Stored images into S3 and generated alternative text for images in form of `[image caption](image link)`.
- Improved the accuracy of text extraction by leveraging LLM to correct spacing and typographical errors by 20%.
- Optimized the response speed by processing the text correcting and image processing parallelly by 67%.

## Challenges
One of the biggest challenges is how to optimize the response speed. 

At first, I just utilized **Azure Computer Vision** to get caption and OCR result of each image and leveraged **OpenAI LLM** `gpt-turbo-3.5` to correct the spacing and typographical errors in text content.

However, as the number of pages in PDF file grows, it takes forever to process one PDF file, since even one API call to OpenAI and Azure CV takes several seconds. So I realized that I need to run these tasks parallelly instead of one by one.

Then here came new problem. Even though OpenAI provides asynchronous support, Azure CV still does not implement it. Therefore, in order to get to improve the response speed. I need to make a tradeoff between abandoning the original plan by adding image processing and figuring out another way to do it.

Fortunately, finally I found [marvin](https://www.askmarvin.ai/docs/vision/captioning/#async-support) toolkit which is based on **OpenAI Vision** and provides pretty good asynchronous support for generating image caption.

By trying so hard to do some optimization, then response speed improved by around 67%, which is pretty satisfying for our current task.

### Feature and Performance Comparison

|                  | PDF Reader                                                                      | Jina Reader                                                    | Amazon Textract                                                                                                                                                                            |
|------------------|---------------------------------------------------------------------------------|----------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| response time    | fast (*)                                                                        | very fast                                                      | very fast                                                                                                                                                                                  |
| response content | Text + Alternative text for all images                                          | Only text content; with a few spacing errors                   | Text + Image                                                                                                                                                                               |
| Cons             | It takes a little longer time if enabling image extraction and text correction. | No image processing; accuracy of text result is not that good. | Only OCR was used vertically to extract all the content in the PDF file. So content would be totally messed up when the document was not strictly formatted vertically from top to bottom. |

Note (*): PDF Reader can reach the same fast speed as Jina Reader if query parameters `image=False` and `correct=False` were set, which disable the two time-consuming features.

## How to Set up

## How to Run

