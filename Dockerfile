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
