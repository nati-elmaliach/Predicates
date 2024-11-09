FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/Predicates"
ENV PREDICATE_SERVICE_URL=http://localhost:5000

# Set working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run the application
CMD ["python3", "src/remote/index.py"]
