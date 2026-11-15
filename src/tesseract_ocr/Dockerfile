# Images are pinned by tag + digest; Dependabot keeps both up to date
FROM ghcr.io/astral-sh/uv:0.13.8@sha256:5cc1805e2426484abca4ad46ea783bab281fdb225fd82d8ce6d66a81254bac85 AS uv

# ---- Base Image ----
FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928 AS base

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
