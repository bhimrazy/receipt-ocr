# ---- Base Image ----
FROM python:3.12-slim AS base

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UV_EXTRA_INDEX_URL="https://pypi.org/simple"

# ---- Builder ----
FROM base AS builder

# Install uv
RUN pip install uv

# Create a virtual environment
RUN uv venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN uv pip install --no-cache-dir -r requirements.txt

# ---- Runner ----
FROM base AS runner

# Create a non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Copy the virtual environment from the builder
COPY --from=builder /opt/venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/home/appuser

# Copy the application code
COPY . tesseract_ocr

# Expose the port
EXPOSE 80

# Run the application
CMD ["uvicorn", "tesseract_ocr.app:app", "--host", "0.0.0.0", "--port", "80"]
