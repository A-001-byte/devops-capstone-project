FROM python:3.11-slim

# Set up the working directory
WORKDIR /app

# Install the Python dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service source code
COPY service/ ./service/
COPY wsgi.py .

# Run as a non-root user
RUN useradd --uid 1000 theia && chown -R theia /app
USER theia

# The service listens on port 8080
EXPOSE 8080
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "wsgi:app"]
