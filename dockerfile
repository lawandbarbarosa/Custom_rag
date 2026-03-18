FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p temp_uploads

# Match your code's port
EXPOSE 8001

# Use double quotes and the correct filename (api.py)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]