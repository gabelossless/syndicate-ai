# ---- Syndicate.ai Production Backend ---- #
# Base image optimized for Python + FastAPI
FROM python:3.11-slim-bookworm

# Set work directory
WORKDIR /app

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for mutegen/cryptography
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies execution
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (Cloud providers like Railway/Render use dynamic $PORT, but we expose 8000 as default)
EXPOSE 8000

# Start Uvicorn loop 
# (Note: In production, you would bind to PostgreSQL via DATABASE_URL env var instead of local sqlite)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
