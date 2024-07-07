# pdf-reader

## Introduction
This project aims to serve as middleware between an original PDF file and being used to construct knowledge base in [dify](https://dify.ai/). However, I hope it has more than that.


## Highlights
- Leveraged Langchain PyPDFLoader to process PDF document in chunks.
- Utilized OCR to extract text content from PDF file.
- Stored the images into S3 and generated alternative text for images in form of `[image caption](image link): image OCR content`.
- Improved the accuracy of text extraction by leveraging LLM to correct spacing and typographical errors.
- Optimized the response speed by processing the text correcting and image processing parallelly. (still working on)

### Feature and Performance Comparison

|                | PDF reader                                | Jina Reader          | Amazon Textract                                                                                                                                                                   |
|----------------|-------------------------------------------|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| response time  | normal                                    | fast                 | fast                                                                                                                                                                              |
| response content | Text + Alternative text for all images    | Only text content   | Text + Image                                                                                                                                                                      |
| issues         | It takes a little longer time to process. | No image processing. | Only OCR was used vertically to extract all the content in the PDF file. So content would be totally messed up when the document was not strictly formatted vertically from top to bottom. |

## How to Set up

## How to Run

