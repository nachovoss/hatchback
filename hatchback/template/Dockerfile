FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change ownership of the application files
RUN chown -R app:app /app

# Switch to non-root user
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
