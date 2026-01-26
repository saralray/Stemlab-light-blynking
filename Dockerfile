FROM python:3.11-slim

# Prevent Python from swallowing signals
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose Flask port
EXPOSE 5000

# Use exec form so SIGINT works
CMD ["python", "app.py"]
