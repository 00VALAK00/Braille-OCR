FROM python:3.11-slim

LABEL authors="Iheb"

WORKDIR /app

COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-setuptools \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt



# Set environment variables
ENV LANGUAGE=en \
    SEGMENT=False \
    ANALYSE=True


CMD python3 main.py -d "$DIRECTORY" -l "$LANGUAGE" -s "$SEGMENT" --analyse "$ANALYSE"

