FROM bitnami/spark:3.5

USER root

WORKDIR /app

COPY requirements_processing.txt .
RUN pip install --no-cache-dir -r requirements_processing.txt

COPY spark_processing.py .

CMD ["spark-submit", "spark_processing.py"]
