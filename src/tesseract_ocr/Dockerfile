# Images are pinned by tag + digest; Dependabot keeps both up to date
FROM ghcr.io/astral-sh/uv:0.12.23@sha256:61d393e44e249f2e4b526b6c7ddcecce245946826e608e11c93ad4f5bba55b21 AS uv

# ---- Base Image ----
FROM python:3.12-slim@sha256:ddb0207ae1f0356c2b724d740769b0c5f5f51cc54a0525178f721825f78fe74c AS base

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ---- Builder ----
FROM base AS builder

# Install uv
COPY --from=uv /uv /bin/uv

# requirements.txt is unpinned: skip releases newer than this (supply-chain guard).
# Build-time only; override with --build-arg UV_EXCLUDE_NEWER=...
ARG UV_EXCLUDE_NEWER="2 days"

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
