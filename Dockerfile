FROM python:3.11-slim
#FROM python:3.11-alpine

WORKDIR /app

# System dependencies for PyMuPDF
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Copy all project files into the image
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Hugging Face expects app to listen on this port
ENV PORT=7860
EXPOSE 7860

# Start the Flask app with gunicorn on port 7860
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:7860"]
