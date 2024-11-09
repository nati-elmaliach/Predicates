FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/Predicates"
ENV PREDICATE_SERVICE_URL=http://localhost:5000

# Set working directory
WORKDIR /app

# Copy only the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the container
COPY . /app

# Set permissions for the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
