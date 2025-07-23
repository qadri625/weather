# Use a lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OPENWEATHER_API_KEY=your_api_key_here

# Set working directory
WORKDIR /app

# Copy app files
COPY app/ /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the app port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

