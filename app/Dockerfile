FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Set the PATH to include the virtual environment binaries.
ENV PATH="/app/.venv/bin:$PATH"

# Run the application.
CMD ["fastapi", "run", "server.py", "--port", "8000", "--host", "0.0.0.0"]
