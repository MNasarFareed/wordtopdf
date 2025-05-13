FROM python:3.11-slim

# Install LibreOffice
RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-core libreoffice-writer && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy project
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
