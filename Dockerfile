name: CI/CD Pipeline

on:
  push:
    branches:
      - master

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1

    - name: Login to AWS ECR
      run: |
        aws ecr get-login-password --region YOUR_REGION | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com

    - name: Build, tag, and push the image to ECR
      run: |
        docker build -t fastapi-lambda-app .
        docker tag fastapi-lambda-app:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/fastapi-lambda-app:latest
        docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/fastapi-lambda-app:latest

    - name: Update Lambda Function
      run: |
        aws lambda update-function-code --function-name YOUR_LAMBDA_FUNCTION_NAME --image-uri YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/fastapi-lambda-app:latest
