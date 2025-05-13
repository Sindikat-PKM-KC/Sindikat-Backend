# Dockerfile
FROM python:3.11-slim-bullseye

RUN apt-get update && \
    apt-get install -y gcc libpq-dev nginx && \
    pip install --upgrade pip

# Copy requirements and install Python packages
COPY ./project/requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY ./project /app
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf

# Create static/media dirs if not exists
RUN mkdir -p /app/static /app/media

# Copy entrypoint
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose only Nginx port
EXPOSE 80

WORKDIR /app

ENTRYPOINT [ "sh", "/entrypoint.sh" ]
