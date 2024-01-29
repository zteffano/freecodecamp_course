FROM python:3.10-slim-bullseye

# Update and install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev pkg-config \
    && pip install --no-cache-dir --upgrade pip

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy the rest of your application
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python3", "server.py"]
