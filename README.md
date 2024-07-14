# PDF Reader

All the files (except .gitignore) listed in this branch are needed for deployment. The only thing you need to change is the `.env` file. You need to fill out the values of environment variables with your own API keys or desired values.

Mine is hosted at https://nv27s8zxgi.execute-api.us-west-1.amazonaws.com/prod/. (still working the domain name)

Be aware that the PDF extraction service is not open for the public yet (due to financial and permission issue), which means specific token will be needed for the response of PDF extraction. If you really need this service, you can host it on your own since all the project codes are already open-source.


## How to Deploy
We are going to deploy this project using [AWS Lambda](https://aws.amazon.com/lambda/), a serverless compute service, which means we don't need to manage servers and clusters, the cloud service provider (CSP, in this case i.e. AWS) manages the infrastructure required to run the code, including provisioning, scaling, and runtime environments.

Since the project's dependency package size exceeds the AWS Lambda layer limit, complicating dependency management with AWS Layers, we will use a container image to build the Lambda function.

### 1. Prepare a Dockerfile
 ```dockerfile
 # Use an official Python runtime as a base image
 FROM public.ecr.aws/lambda/python:3.10
 
 # Copy the requirements file into the container
 COPY requirements.txt ${LAMBDA_TASK_ROOT}
 
 # Install dependencies (--no-cache-dir -> can reduce the size of packages)
 RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt
 
 # Copy function code
 COPY . ${LAMBDA_TASK_ROOT}
 
 # Run the FastAPI server
 CMD [ "main.handler" ]
 ```
- `LAMBDA_TASK_ROOT` is pre-defined environment variable of [AWS base image for Python 3.10](https://github.com/aws/aws-lambda-base-images/blob/python3.10/Dockerfile.python3.10).


### 2. Build Docker Image
 ```bash
 docker build -t pdf-extraction-service .
 ```
### 3. Push the Image to AWS ECR

While in this step, please create an ECR repository before you start. Record the repo name because you are going to use it for tagging the image and pushing the image to this repo.

- Log in to ECR
 ```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
   ```
   
- Tag your docker image with `latest` 
 ```bash
 docker tag pdf-extraction-service:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<ecr-repo-name>:latest
 ```
   
- Push the docker image to ECR
 ```bash
 docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<ecr-repo-name>:latest
 ```
### 4. Create Lambda Function with ECR Image

Create a lambda function with "Container image" in the top, and entered the ECR image URI built in step 3.

**In this step, in order to make sure the lambda function can have access to put object into S3 bucket, you need to add `AmazonS3FullAccess` permission to the execution role of the lambda function.**

### 5. Configure API Gateway

In order to make your lambda function accessibly with HTTP, you can create Rest API with API Gateway. You can check out [AWS API Gateway REST APIS](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-develop.html) and follow the steps to implement this.