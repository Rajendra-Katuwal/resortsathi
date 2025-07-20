# Use official Python image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# # Collect static files
# RUN python manage.py collectstatic --noinput

# Run gunicorn server
CMD ["gunicorn", "restrosathi.wsgi:application", "--bind", "0.0.0.0:8000"]
