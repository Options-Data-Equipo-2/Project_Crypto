FROM python:3.11-slim

WORKDIR /app

COPY requirements_ingest.txt .
RUN pip install --no-cache-dir -r requirements_ingest.txt

COPY ingest_stock.py .

CMD ["python", "ingest_stock.py"]
