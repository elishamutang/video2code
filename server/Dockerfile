# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

COPY . .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

# Run stage
FROM python:3.11-slim AS runner

# Install Tesseract OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app /app
RUN pip install --no-cache /wheels/* && rm -rf /wheels

WORKDIR /app/adv_ui_ocrroo_project

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "adv_ui_ocrroo_project.wsgi"]