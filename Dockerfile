# Use Python 3.11 base image
FROM python:3.11-slim

# Install dependencies Pillow and others need
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install Python packages
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . /app

# Expose Flask port
EXPOSE 5000

# Command to start your Flask app
# replace previous CMD with this
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "2", "--timeout", "120"]

