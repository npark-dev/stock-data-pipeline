# Stock Data Pipeline Project

A data pipeline project for collecting and processing real-time stock market data

## Infrastructure Components

- MinIO (Data Lake)
- PostgreSQL (Data Warehouse)
- Apache Kafka (Streaming)
- Apache Airflow (Orchestration)

## Setup Instructions

1. Prerequisites
   - Docker
   - Python 3.9+
   - WSL2 (Windows users)

2. Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start services
docker-compose up -d

