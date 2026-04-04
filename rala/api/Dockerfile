FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all python source files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# By default, run the API (this will be overridden by docker-compose for workers)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
