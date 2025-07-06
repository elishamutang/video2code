# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

COPY adv_ui_ocrroo_project/ adv_ui_ocrroo_project/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

# Run stage
FROM python:3.11-slim AS runner

# Install Tesseract OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

EXPOSE 8000

WORKDIR /app/adv_ui_ocrroo_project

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "adv_ui_ocrroo_project.wsgi"]