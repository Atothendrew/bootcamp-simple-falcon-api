# python3.6 -m venv venv
FROM python:3.6

# Common practice is to update all packages
RUN apt-get update -y

# Create a directory to store our code
RUN mkdir /app

# Copy our requirements first, so that this layer is cached
COPY requirements.txt /app/

# Install our requirements
RUN pip install -r /app/requirements.txt

# Copy the rest of our app
COPY . /app

# Tell docker to use the /app folder as our working directory
WORKDIR /app

# Install our package
RUN python setup.py clean --all install clean --all

# Run the command
ENV API_PORT 8000
CMD gunicorn --preload --bind=0.0.0.0:$API_PORT simple_storage_api.api:api
