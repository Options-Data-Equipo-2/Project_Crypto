FROM python:3.11-slim

USER root

WORKDIR /app

COPY requirements_processing.txt .
RUN pip install --no-cache-dir -r requirements_processing.txt

COPY spark_processing.py .

CMD ["python", "spark_processing.py"]
