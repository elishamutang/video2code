# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

COPY . .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

# Stage 2: Run stage
FROM python:3.11-slim AS runner

# Install Tesseract OCR and gosu
RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1-mesa-glx gosu && \
    rm -rf /var/lib/apt/lists/*

# Accept UID and GID as build arguments
ARG UID=1000
ARG GID=1000

# Create non-root user and group with specified UID/GID
RUN groupadd -g $GID appuser && useradd -m -u $UID -g $GID appuser

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app /app

# Install dependencies as root
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# Copy entrypoint script and make it accessible
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint to the script
ENTRYPOINT [ "/entrypoint.sh" ]

WORKDIR /app/adv_ui_ocrroo_project

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "adv_ui_ocrroo_project.wsgi"]