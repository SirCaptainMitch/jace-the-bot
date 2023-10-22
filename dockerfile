# Use the official Python image as base image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry install --no-root --only main

# Expose port for Streamlit
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Set the environment variables
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Run the app with streamlit command
#ENTRYPOINT ["poetry", "run"]


