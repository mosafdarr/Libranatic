# Use official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.12

# Set working directory in the container
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy project files first
COPY pyproject.toml poetry.lock README.md ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the current directory contents into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["index.handler"]
