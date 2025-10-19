# Build from base image
FROM python:3.10-slim-bullseye 

# Install OS dependencies. Avoid installing unnecessary additional packages, and avoid extra space used for caching
# Keep these commands together so its all a single image layer
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev \
  && pip install --no-cache-dir --upgrade pip

# Create a dir for your application source to live
WORKDIR /app

# Copy the requirements.txt and pip install in your image
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy source code into container
COPY . /app

# Doesn't do anything, but just documents that you are planning to serve on port 5000
EXPOSE 5000

# Run container
CMD ["python3", "server.py"]
