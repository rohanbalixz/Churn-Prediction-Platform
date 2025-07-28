# Use official slim Python image
FROM python:3.10-slim

# Install Java (needed for Spark/Delta)
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    rm -rf /var/lib/apt/lists/*

# Point JAVA_HOME (if Spark needs it)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install \
    delta-spark \
    pyspark \
    fastapi \
    uvicorn \
    xgboost \
    tensorflow \
    pandas \
    numpy \
    scikit-learn \
    pyarrow \
    fastparquet \
    requests

# Copy your project files
WORKDIR /app
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the API
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
