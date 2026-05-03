FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    procps \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

COPY requirements_processing.txt .

RUN pip install --no-cache-dir -r requirements_processing.txt

COPY spark_processing.py .

CMD ["python", "spark_processing.py"]
