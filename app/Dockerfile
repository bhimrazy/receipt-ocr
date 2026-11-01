# Images are pinned by tag + digest; Dependabot keeps both up to date
FROM ghcr.io/astral-sh/uv:0.13.6@sha256:af22a52f5eafef3d78e551599d405c02df61919d18028f0cea8eda93bc9986d0 AS uv

FROM python:3.12-slim@sha256:ddb0207ae1f0356c2b724d740769b0c5f5f51cc54a0525178f721825f78fe74c

# Install uv.
COPY --from=uv /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Set the PATH to include the virtual environment binaries.
ENV PATH="/app/.venv/bin:$PATH"

# Run the application.
CMD ["fastapi", "run", "server.py", "--port", "8000", "--host", "0.0.0.0"]
